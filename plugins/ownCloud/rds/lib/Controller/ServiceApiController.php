<?php

namespace OCA\RDS\Controller;

use OCP\IRequest;
use OCP\AppFramework\ApiController;
use OCP\AppFramework\Http;
use OCP\AppFramework\Http\JSONResponse;

class ServiceApiController extends ApiController
{
    private $rdsURL = "https://sciebords-dev.uni-muenster.de/token-service";
    private $userId;
    
    public function __construct($AppName, IRequest $request, $userId)
    {
        parent::__construct($AppName, $request);
        $this->userId = $userId;
    }

    /**
     * Returns a list with all services from RDS.
     * 
     * @return array a list with object with key "jwt", see $this->show()
     * 
     * @NoAdminRequired
     * @NoCSRFRequired
     */
    public function index()
    {
        $url = $this->rdsURL . "/service";

        $curl = curl_init();
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_URL, $url);
        curl_setopt($curl, CURLOPT_ENCODING , "gzip");
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
        $result = curl_exec($curl);
        $response = json_decode($result, true);
        $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        curl_close($curl);

        if($httpcode >= 300) {
            return new JSONResponse();
        }

        $listOfServices = [];

        foreach ((array) $response as $element) {
            $jwt = $element["jwt"];
            # decode jwt
            $pieces = explode(".", $jwt);
            $decode = base64_decode($pieces[1], true);
            $payload = json_decode($decode, true);
            $obj = array(
                "servicename" => $payload["servicename"],
                "authorize_url" => urldecode($payload["authorize_url"]),
                "state" => base64_encode(json_encode(["jwt" => $jwt, "user" => $this->userId]))
            );
            $listOfServices[] = $obj;
        }

        return new JSONResponse($listOfServices);
    }

    /**
     * Returns a single service from RDS to authenticate with.
     * 
     * @param string $servicename
     * @return object an object with jwt encoded object {"servicename", "authorize_url", "date"}
     *
     * @NoAdminRequired
     */
    public function show($servicename)
    {
        $url = $this->rdsURL . "/service/" . $servicename;

        $curl = curl_init();
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_URL, $url);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
        $result = curl_exec($curl);
        $response = json_decode($result, true);
        $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        curl_close($curl);

        if($httpcode >= 300) {
            return new JSONResponse();
        }
        
        $jwt = $response["jwt"];
        # decode jwt
        $pieces = explode(".", $jwt);
        $decode = base64_decode($pieces[1], true);
        $payload = json_decode($decode, true);
        $obj = array(
            "servicename" => $payload["servicename"],
            "authorize_url" => urldecode($payload["authorize_url"]),
            "state" => $jwt
        );

        return new JSONResponse($obj);
    }

    /**
     * Removes a single service from the user in RDS.
     *
     * @param string $servicename
     * @return bool returns true for success, else false
     *
     * @NoAdminRequired
     */
    public function removeServiceFromUser($servicename)
    {
        $curl = curl_init($this->rdsURL . "/user/" . $this->userId . "/service/" . $servicename);
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => "DELETE"];
        curl_setopt_array($curl, $options);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);

        $response = json_decode(curl_exec($curl));
        $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        curl_close($curl);

        if($httpcode >= 300) {
            return new JSONResponse();
        }

        return new JSONResponse($response);
    }


    /**
     * Returns a list with all services from rds, which registered for user.
     * 
     * @return string a list of strings, which are servicenames
     *
     * @NoAdminRequired
     */
    public function getRegisteredServicesForUser()
    {
        $curl = curl_init($this->rdsURL . "/user/" . $this->userId . "/service");
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);

        $response = json_decode(curl_exec($curl));
        $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        curl_close($curl);

        if($httpcode >= 300) {
            return new JSONResponse([]);
        }

        return new JSONResponse($response->list);
    }
}

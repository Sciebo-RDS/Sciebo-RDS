<?php

namespace OCA\RDS\Controller;

use OCP\IRequest;
use OCP\AppFramework\ApiController;
use OCP\AppFramework\Http;
use OCP\AppFramework\Http\JSONResponse;

class ServiceApiController extends ApiController
{
    private $rdsURL = "http://sciebords-dev.uni-muenster.de";
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
     */
    public function index()
    {
        $curl = curl_init($this->rdsURL + "/service");
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

        $response = json_decode(curl_exec($curl));
        curl_close($curl);

        $listOfServices = [];

        foreach ($response as $jwt) {
            # decode jwt
            $pieces = explode(".", $response);
            $payload = base64_decode($pieces[1]);
            $payload = json_decode($payload);
            $payload->state = $jwt;
            $listOfServices[] = $payload;
        }

        return new JSONResponse($listOfServices);
    }

    /**
     * Returns a single service from RDS to authenticate with.
     * 
     * @param int $servicename
     * @return object an object with jwt encoded object {"servicename", "authorize_url", "date"}
     *
     * @NoAdminRequired
     */
    public function show($servicename)
    {
        $curl = curl_init($this->rdsURL + "/service/" + $servicename);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

        $response = json_decode(curl_exec($curl));
        curl_close($curl);

        return new JSONResponse($response);
    }

    /**
     * Removes a single service from the user in RDS.
     *
     * @param int $servicename
     * @return bool returns true for success, else false
     *
     * @NoAdminRequired
     */
    public function removeServiceFromUser($servicename)
    {
        $curl = curl_init($this->rdsURL + "/user/" + $this->userId + "/service/" + $servicename);
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => "DELETE"];
        curl_setopt_array($curl, $options);

        $response = json_decode(curl_exec($curl));
        curl_close($curl);

        return new JSONResponse($response);
    }


    /**
     * Returns a list with all services from rds, which registered for user.
     * 
     * @param int $servicename
     * @return string a list of strings, which are servicenames
     *
     * @NoAdminRequired
     */
    public function getRegisteredServicesForUser()
    {
        $curl = curl_init($this->rdsURL + "/user/" + $this->userId);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

        $response = json_decode(curl_exec($curl));
        curl_close($curl);

        return JSONResponse($response);
    }
}

<?php

namespace OCA\RDS\Db;

use \OCA\RDS\Db\Service;
use \OCA\RDS\Db\RegisteredService;
use \OCA\RDS\Service\NotFoundException;
use \OCA\RDS\Service\UrlService;

class ServiceMapper
{
    private $urlService;
    private $userId;

    public function __construct(UrlService $urlService, $userId)
    {
        $this->urlService = $urlService;
        $this->userId = $userId;
    }

    public function findAll()
    {
        $url = $this->urlService->getPortURL() . '/service';

        $curl = curl_init();
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_URL, $url);
        curl_setopt($curl, CURLOPT_ENCODING, 'gzip');
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
        $result = curl_exec($curl);
        $response = json_decode($result, true);
        $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        $info = curl_getinfo($curl);
        curl_close($curl);

        if ($httpcode >= 300) {
            throw new NotFoundException(json_encode([
                'http_code' => $httpcode,
                'json_error_message' => json_last_error_msg(),
                'curl_error_message' => $info
            ]));
        }

        $listOfServices = [];

        foreach ((array) $response as $element) {
            $jwt = $element['jwt'];
            # decode jwt
            $pieces = explode('.', $jwt);
            $decode = base64_decode($pieces[1], true);
            $payload = json_decode($decode, true);

            $svc = new Service();
            $svc->setServicename($payload['servicename']);
            $svc->setAuthorizeUrl(urldecode($payload['authorize_url']));

            $svc->setState($jwt);
            $listOfServices[] = $svc;
        }

        return $listOfServices;
    }

    public function find($servicename)
    {
        $url = $this->urlService->getPortURL() . '/service/' . $servicename;

        $curl = curl_init();
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_URL, $url);
        curl_setopt($curl, CURLOPT_ENCODING, 'gzip');
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
        $result = curl_exec($curl);
        $response = json_decode($result, true);
        $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        $info = curl_getinfo($curl);
        curl_close($curl);

        if ($httpcode >= 300) {
            throw new NotFoundException(json_encode([
                'http_code' => $httpcode,
                'json_error_message' => json_last_error_msg(),
                'curl_error_message' => $info
            ]));
        }

        $jwt = $response['jwt'];
        # decode jwt
        $pieces = explode('.', $jwt);
        $decode = base64_decode($pieces[1], true);
        $payload = json_decode($decode, true);

        $svc = new Service();
        $svc->setServicename($payload['servicename']);
        $svc->setAuthorizeUrl(urldecode($payload['authorize_url']));

        $svc->setState($jwt);

        return $svc;
    }
}

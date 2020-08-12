<?php

namespace OCA\RDS\Db;

use \OCA\RDS\Db\RegisteredService;
use \OCA\RDS\Db\Project;
use \OCA\RDS\Service\NotFoundException;
use \OCA\RDS\Service\UrlService;


class UserserviceMapper
{
    private $urlService;

    public function __construct(UrlService $urlService)
    {
        $this->urlService = $urlService;
    }

    # this should be the way to add a service to rds

    public function insert($userId)
    {
        #TODO: create a new connection in RDS and return it
        return [];
    }

    # not used. if you want to update a service, you have to delete it first

    public function update($servicename, $userId)
    {
        return [];
    }

    public function delete($servicename, $userId)
    {
        $svc = $this->find($servicename, $userId);

        $curl = curl_init($this->urlService->getPortURL() . '/user/' . $userId . '/service/' . $servicename);
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => 'DELETE'];
        curl_setopt_array($curl, $options);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);

        $response = json_decode(curl_exec($curl));
        $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        curl_close($curl);

        return $svc;
    }

    public function findAll($userId)
    {
        $curl = curl_init($this->urlService->getPortURL() . '/user/' . $userId . '/service');
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);

        $response = json_decode(curl_exec($curl), true);
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
        $res = $response['list'];

        foreach ((array) $res as $element) {
            $svc = new RegisteredService();

            $svc->setServicename($element['servicename']);
            $svc->setUserId($userId);
            $svc->setAccessToken($element['access_token']);
            $svc->setServiceProjects($element['projects']);

            $type = [];
            foreach ($element['implements'] as $value) {
                switch ($value) {
                    case 'fileStorage':
                        $type['fileStorage'] = true;
                        break;
                    case 'metadata':
                        $type['metadata'] = true;
                        break;
                }
            }

            $svc->setType($type);

            $listOfServices[] = $svc;
        }

        return $listOfServices;
    }

    public function find($servicename, $userId)
    {
        $services = $this->findAll($userId);

        foreach ($services as $element) {
            if ($element->getServicename() == $servicename) {
                return $element;
            }
        }

        throw new NotFoundException('Service ' . $servicename . ' not found.');
    }

    public function register($servicename, $code, $state, $userId, $secret)
    {
        function jwt_encode($arr)
        {
            # inspired by https://rbrt.wllr.info/2018/01/29/how-create-json-web-token-php.html
            if (is_array(($arr))) {
                $val = json_encode($arr);
            } else {
                $val = $arr;
            }

            $base64 = base64_encode($val);
            $base64url =  str_replace(['+', '/', '='], ['-', '_', ''], $base64);
            return ($base64url);
        }

        $head = ['alg' => 'HS256', 'typ' => 'JWT'];
        $body = ['servicename' => $servicename, 'code' => $code, 'state' => $state, 'userId' => $userId];

        $jwtHead = jwt_encode($head);
        $jwtBody = jwt_encode($body);
        $sign = hash_hmac('sha256', $jwtHead . "." . $jwtBody, $secret, true);
        $jwtSign = jwt_encode($sign);

        $jwt =  $jwtHead . '.' . $jwtBody . '.' . $jwtSign;

        $url = $this->urlService->getPortURL() . '/exchange';

        $curl = curl_init();
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => 'POST'];
        curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode(['jwt' => $jwt]));
        curl_setopt($curl, CURLOPT_URL, $url);
        curl_setopt($curl, CURLOPT_ENCODING, 'gzip');
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
        curl_setopt($curl, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
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

        return true;
    }
}

<?php
namespace OCA\RDS\Db;

use \OCA\RDS\Db\Service;
use \OCA\RDS\Db\RegisteredService;
use \OCA\RDS\Service\NotFoundException;

class UserserviceMapper {
    private $rdsURL = 'https://sciebords-dev.uni-muenster.de/token-service';

    public function __construct() {

    }

    # this should be the way to add a service to rds

    public function insert( $userId ) {
        #TODO: create a new connection in RDS and return it
        return [];
    }

    # not used. if you want to update a service, you have to delete it first

    public function update( $servicename, $userId ) {
        return [];
    }

    public function delete( $servicename, $userId ) {
        $svc = $this->find( $servicename, $userId );

        $curl = curl_init( $this->rdsURL . '/user/' . $userId . '/service/' . $servicename );
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => 'DELETE'];
        curl_setopt_array( $curl, $options );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $response = json_decode( curl_exec( $curl ) );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        curl_close( $curl );

        return $svc;
    }

    public function findAll( $userId ) {
        $curl = curl_init( $this->rdsURL . '/user/' . $userId . '/service' );
        curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $response = json_decode( curl_exec( $curl ) );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        $info = curl_getinfo( $curl );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            throw new NotFoundException( json_encode( [
                'http_code'=>$httpcode,
                'json_error_message'=>json_last_error_msg,
                'curl_error_message'=>$info
            ] ) );
        }

        $listOfServices = [];

        foreach ( ( array )$response['list'] as $element ) {
            $svc = new RegisteredService();

            $svc->setServicename( $element['servicename'] );
            $svc->setUserId( $userId );
            $svc->setAccessToken( $element['access_token'] );
            $svc->setServiceProjects( $element['projects'] );

            $listOfServices[] = $svc;
        }

        return $listOfServices;
    }

    public function find( $servicename, $userId ) {
        $curl = curl_init( $this->rdsURL . '/user/' . $userId . '/service/' . $servicename );
        curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $response = json_decode( curl_exec( $curl ) );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        $info = curl_getinfo( $curl );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            throw new NotFoundException( json_encode( [
                'http_code'=>$httpcode,
                'json_error_message'=>json_last_error_msg,
                'curl_error_message'=>$info
            ] ) );
        }

        $svc = new RegisteredService();

        $svc->setServicename( $response['servicename'] );
        $svc->setUserId( $userId );
        $svc->setAccessToken( $response['access_token'] );
        $svc->setServiceProjects( $response['projects'] );

        return $svc ;
    }
}
<?php
namespace OCA\RDS\Db;

use OCA\RDS\Db\Service;
use OCA\RDS\Db\RegisteredService;

class ServiceMapper {
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

    public function getAllServices() {
        $url = $this->rdsURL . '/service';

        $curl = curl_init();
        curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );
        curl_setopt( $curl, CURLOPT_URL, $url );
        curl_setopt( $curl, CURLOPT_ENCODING, 'gzip' );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );
        $result = curl_exec( $curl );
        $response = json_decode( $result, true );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            return  [];
        }

        $listOfServices = [];

        foreach ( ( array ) $response as $element ) {
            $jwt = $element['jwt'];
            # decode jwt
            $pieces = explode( '.', $jwt );
            $decode = base64_decode( $pieces[1], true );
            $payload = json_decode( $decode, true );

            $svc = new Service();
            $svc->setServicename( $payload['servicename'] );
            $svc->setAuthorizeUrl( urldecode( $payload['authorize_url'] ) );

            /* FIXME: Level HIGH, Add here security for userid, otherwise a rouge can register his own service account for another user.
            Any ideas? pub/priv keys, send current oauth token to verify the request, that it comes from owncloud? encrypt it with AES with client-secret as password? */
            $svc->setState( base64_encode( json_encode( ['jwt' => $jwt, 'user' => $userId] ) ) );
            $listOfServices[] = $svc;
        }

        return $listOfServices;
    }

    public function findAll( $userId ) {
        $curl = curl_init( $this->rdsURL . '/user/' . $userId . '/service' );
        curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $response = json_decode( curl_exec( $curl ) );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            return NULL;
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
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            return NULL;
        }

        $svc = new RegisteredService();

        $svc->setServicename( $response['servicename'] );
        $svc->setUserId( $userId );
        $svc->setAccessToken( $response['access_token'] );
        $svc->setServiceProjects( $response['projects'] );

        return $svc ;
    }
}
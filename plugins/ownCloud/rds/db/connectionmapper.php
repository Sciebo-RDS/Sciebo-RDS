<?php
namespace OCA\RDS\Db;

use OCA\RDS\Db\Connection;

class ConnectionMapper {
    private $rdsURL = 'https://sciebords-dev.uni-muenster.de/project';

    public function __construct() {

    }

    public function insert( $userId ) {
        $curl = curl_init( $this->rdsURL . '/user/' . $this->userId );
        $options = [CURLOPT_RETURNTRANSFER => true];
        curl_setopt_array( $curl, $options );
        curl_setopt( $cnxn, CURLOPT_POST, TRUE );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $response = json_decode( curl_exec( $curl ) );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            return NULL;
        }

        return array_slice( $this->findAll( $conn->userId ), -1 );
    }

    public function update( $conn ) {
        $curl = curl_init( $this->rdsURL . '/user/' . $this->userId . '/project/' . $projectIndex );
        $options = [CURLOPT_RETURNTRANSFER => true];
        curl_setopt_array( $curl, $options );
        curl_setopt( $curl, CURLOPT_POSTFIELDS, $conn->jsonSerialize() );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $response = json_decode( curl_exec( $curl ) );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            return NULL;
        }

        return $this->find( $conn->projectIndex, $conn->userId );
    }

    public function delete( $projectIndex, $userId ) {
        $conn = $this->find( $projectIndex, $userId );

        $curl = curl_init( $this->rdsURL . '/user/' . $this->userId . '/project/' . $projectIndex );
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => 'DELETE'];
        curl_setopt_array( $curl, $options );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $response = json_decode( curl_exec( $curl ) );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            return NULL;
        }

        return $conn;
    }

    public function find( $projectIndex, $userId ) {
        $url = $this->rdsURL . '/user/' . $userId . '/project/' . $projectIndex;

        $curl = curl_init();
        curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );
        curl_setopt( $curl, CURLOPT_URL, $url );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );
        $result = curl_exec( $curl );
        $response = json_decode( $result, true );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            return NULL;
        }

        $conn = new Connection();
        $conn->setUserid( $response['userId'] );
        $conn->setStatus( $response['status'] );
        $conn->setProjectId( $response['projectId'] );
        $conn->setProjectIndex( $response['projectIndex'] );
        $conn->setPortIn( $response['portIn'] );
        $conn->setPortOut( $response['portOut'] );

        return $conn;
    }

    public function findAll( $userId ) {
        $url = $this->rdsURL . '/user/' . $userId;

        $curl = curl_init();
        curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );
        curl_setopt( $curl, CURLOPT_URL, $url );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );
        $result = curl_exec( $curl );
        $response = json_decode( $result, true );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            return NULL;
        }

        $result = [];

        foreach ( $response as $rdsConn ) {
            $conn = new Connection();
            $conn->setUserid( $rdsConn['userId'] );
            $conn->setStatus( $rdsConn['status'] );
            $conn->setProjectId( $rdsConn['projectId'] );
            $conn->setProjectIndex( $rdsConn['projectIndex'] );
            $conn->setPortIn( $rdsConn['portIn'] );
            $conn->setPortOut( $rdsConn['portOut'] );

            $result[] = $conn;
        }

        return $result;
    }

}
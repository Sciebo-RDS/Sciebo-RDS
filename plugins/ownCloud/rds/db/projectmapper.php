<?php
namespace OCA\RDS\Db;

use \OCA\RDS\Db\RegisteredService;
use \OCA\RDS\Db\Project;
use \OCA\RDS\Service\NotFoundException;

class ProjectMapper {
    private $rdsURL = 'https://sciebords-dev.uni-muenster.de/token-service';

    public function __construct() {

    }

    public function findAll ( $servicename, $userId ) {
        $curl = curl_init( $this->rdsURL . '/user/' . $userId . '/service/'. $servicename . '/projects' );
        curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $response = json_decode( curl_exec( $curl ), true );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        $info = curl_getinfo( $curl );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            throw new NotFoundException( json_encode( [
                'http_code'=>$httpcode,
                'json_error_message'=>json_last_error_msg(),
                'curl_error_message'=>$info
            ] ) );
        }

        $listOfProj = [];

        foreach ( ( array ) $response as $element ) {
            $project = new Project();
            $project->setProjectId( $response['projectId'] );
            $project->setMetadata( $response['metadata'] );

            $listOfProj[] = $project;
        }

        return $listOfProj;
    }

    public function find( $servicename, $userId, $projectId ) {
        $curl = curl_init( $this->rdsURL . '/user/' . $userId . '/service/'. $servicename . '/projects/' . $projectId );
        curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $response = json_decode( curl_exec( $curl ), true );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        $info = curl_getinfo( $curl );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            throw new NotFoundException( json_encode( [
                'http_code'=>$httpcode,
                'json_error_message'=>json_last_error_msg(),
                'curl_error_message'=>$info
            ] ) );
        }

        $project = new Project();
        $project->setProjectId( $response['projectId'] );
        $project->setMetadata( $response['metadata'] );

        return $project;
    }

    public function insert( $servicename, $userId ) {
        $curl = curl_init( $this->rdsURL . '/user/' . $userId . '/service/' . $servicename . '/projects' );
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => 'POST'];
        curl_setopt_array( $curl, $options );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $response = json_decode( curl_exec( $curl ) );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        curl_close( $curl );

        $projs = $this->getProjects( $servicename, $userId );
        $proj = end( ( array_values( $projs ) ) );
        return $proj;
    }

    public function delete( $servicename, $userId, $projectId ) {
        $curl = curl_init( $this->rdsURL . '/user/' . $userId . '/service/' . $servicename . '/projects/' . $projectId );
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => 'DELETE'];
        curl_setopt_array( $curl, $options );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $response = json_decode( curl_exec( $curl ) );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        curl_close( $curl );

        return $httpcode == 204;
    }
}
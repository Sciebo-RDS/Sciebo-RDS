<?php
namespace OCA\RDS\Db;

use \OCA\RDS\Db\Port;
use \OCA\RDS\Db\Research;
use \OCA\RDS\Service\NotFoundException;
use OCP\ILogger;

class ResearchMapper {
    private $rdsURL = 'https://sciebords-dev.uni-muenster.de/research';

    public function __construct( ILogger $logger, $appName ) {
        $this->logger = $logger;
        $this->appName = $appName;
    }

    public function log( $message, $arr ) {
        $this->logger->error( $message, array_merge( ['app' => $this->appName], $arr ) );
    }

    public function insert( $userId ) {
        $curl = curl_init( $this->rdsURL . '/user/' . $userId );
        $options = [CURLOPT_RETURNTRANSFER => true];
        curl_setopt_array( $curl, $options );
        curl_setopt( $curl, CURLOPT_POST, TRUE );
        curl_setopt( $curl, CURLOPT_POSTFIELDS, [] );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $request = curl_exec( $curl );
        $response = json_decode( $request, true );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        $info = curl_getinfo( $curl );

        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            throw new NotFoundException( json_encode( [
                'http_code'=>$httpcode,
                'json_error_message'=>json_last_error_msg(),
                'curl_error_message'=>$info,
                'response'=>$request
            ] ) );
        }

        $conn = new Research();
        $conn->setUserId( $response['userId'] );
        $conn->setStatus( $response['status'] );
        $conn->setResearchId( $response['researchId'] );
        $conn->setResearchIndex( $response['researchIndex'] );
        $conn->setportIn( $response['portIn'] );
        $conn->setportOut( $response['portOut'] );

        return $conn;
    }

    public function update( $conn ) {
        $current = $this->find( $conn->getResearchIndex(), $conn->getUserId() );

        return $this->updateResearch( $current, $conn );
    }

    private function updateResearch( $currentResearch, $newResearch ) {
        if ( $currentResearch->getStatus() != $newResearch->getStatus() ) {
            $newResearch->setStatus( $this->nextStatus( $currentResearch ) );
        }

        $this->removeDistinctPorts( $currentResearch, $newResearch );
        $this->addDistinctPorts( $newResearch, $currentResearch );

        return $newResearch;
    }

    /**
    * Removes all $currentPorts from $conn, which are not in $newPorts
    * or has different properties as defined in $newPorts.
    * Returns TRUE, if something was removed, otherwise FALSE.
    *
    * @param \OCA\RDS\Db\Research $currentConn
    * @param \OCA\RDS\Db\Research $newConn
    * @return boolean
    */

    private function removeDistinctPorts( $currentConn, $newConn ) {
        $removeSth = False;

        $removeIndices = $this->getNotEqualPortIndices( $currentConn->getPortIn(), $newConn->getPortIn() );
        foreach ( array_reverse( $removeIndices ) as $index ) {
            $this->removePortIn( $currentConn, $index );
            $removeSth = TRUE;

        }

        $removeIndices = $this->getNotEqualPortIndices( $currentConn->getPortOut(), $newConn->getPortOut() );
        foreach ( array_reverse( $removeIndices ) as $index ) {
            $this->removePortOut( $currentConn, $index );
            $removeSth = TRUE;
        }

        return $removeSth;
    }

    /**
    * Adds all $currentPorts from $conn, which are not in $newPorts
    * or has different properties as defined in $newPorts
    * Returns TRUE, if something was added, otherwise FALSE.
    *
    * @param \OCA\RDS\Db\Research $currentConn
    * @param \OCA\RDS\Db\Research $newConn
    * @return boolean
    */

    private function addDistinctPorts( $currentConn, $newConn ) {
        $addSth = False;

        $addIndices = $this->getNotEqualPortIndices( $currentConn->getPortIn(), $newConn->getPortIn() );
        foreach ( $addIndices as $index ) {
            $this->addPortIn( $currentConn, $currentConn->getPortIn()[$index] );
            $addSth = TRUE;
        }

        $addIndices = $this->getNotEqualPortIndices( $currentConn->getPortOut(), $newConn->getPortOut() );
        foreach ( $addIndices as $index ) {
            $this->addPortOut( $currentConn, $currentConn->getPortOut()[$index] );
            $addSth = TRUE;
        }

        return $addSth;
    }

    private function getNotEqualPortIndices( $currentPorts, $newPorts ) {
        $returnList = [];
        $index = 0;

        foreach ( $currentPorts as $i ) {
            $found = FALSE;
            foreach ( $newPorts as $j ) {
                if ( $i->getPort() == $j->getPort() ) {
                    if ( ! $i->equal( $j ) ) {
                        $returnList[] = $index;
                    }
                    $found = TRUE;
                }
            }

            if ( !$found ) {
                $returnList[] = $index;
            }
        }

        $this->log( 'getNotEqual: 1 {current}, 2 {new} return {return}', ['current'=>$currentPorts, 'new'=>$newPorts, 'return'=>$returnList] );

        return $returnList;
    }

    private function removePortIn( $conn, $index ) {
        return $this->removePort( $conn->getResearchIndex(), $conn->getUserId(), $index, 'imports' );
    }

    private function removePortOut( $conn, $index ) {
        return $this->removePort( $conn->getResearchIndex(), $conn->getUserId(), $index, 'exports' );
    }

    private function addPortIn( $conn, $port ) {
        return $this->addPort( $conn->getResearchIndex(), $conn->getUserId(), $port, 'imports' );
    }

    private function addPortOut( $conn, $port ) {
        return $this->addPort( $conn->getResearchIndex(), $conn->getUserId(), $port, 'exports' );
    }

    private function removePort( $researchIndex, $userId, $portIndex, $where ) {
        $url = $this->rdsURL . '/user/' . $userId . '/research/' . $researchIndex . '/' . $where.'/'.$portIndex;

        $this->log( 'remove port {port} as where {where} from researchindex {researchIndex} and user {userId}.', ['userId'=>$userId, 'researchIndex'=>$researchIndex, 'port'=>$portIndex, 'where'=>$where] );

        $curl = curl_init( $url );
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => 'DELETE'];
        curl_setopt_array( $curl, $options );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $response = json_decode( curl_exec( $curl ) );
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

        return TRUE;
    }

    private function addPort( $researchIndex, $userId, $port, $where ) {
        $url = $this->rdsURL . '/user/' . $userId . '/research/' . $researchIndex . '/' . $where;
        $data_string = json_encode( $port->jsonSerialize() );

        $this->log( 'add port {port} as where {where} for user {userId} and {researchIndex}.', ['userId'=>$userId, 'researchIndex'=>$researchIndex, 'port'=>$data_string, 'where'=>$where] );

        $curl = curl_init( $url );
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => 'POST'];
        curl_setopt( $curl, CURLOPT_HTTPHEADER, array(
            'Content-Type: application/json',
            'Content-Length: ' . strlen( $data_string ) )
        );

        curl_setopt_array( $curl, $options );
        curl_setopt( $curl, CURLOPT_POSTFIELDS, $data_string );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $request = curl_exec( $curl );
        $response = json_decode( $request );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        $info = curl_getinfo( $curl );

        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            throw new NotFoundException( json_encode( [
                'http_code'=>$httpcode,
                'json_error_message'=>json_last_error_msg(),
                'curl_error_message'=>$info,
                'content'=>$request
            ] ) );
        }

        return TRUE;
    }

    private function nextStatus( $conn ) {
        $url = $this->rdsURL . '/user/' . $conn->getUserId() . '/research/' . $conn->getResearchIndex() . '/status';

        $curl = curl_init( $url );
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => 'PATCH'];
        curl_setopt_array( $curl, $options );
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

        return $response['status'];
    }

    public function delete( $researchIndex, $userId ) {
        $conn = $this->find( $researchIndex, $userId );

        $curl = curl_init( $this->rdsURL . '/user/' . $userId . '/research/' . $researchIndex );
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => 'DELETE'];
        curl_setopt_array( $curl, $options );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $request = curl_exec( $curl );
        $response = json_decode( $request );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        $info = curl_getinfo( $curl );

        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            throw new NotFoundException( json_encode( [
                'http_code'=>$httpcode,
                'json_error_message'=>json_last_error_msg(),
                'curl_error_message'=>$info,
                'content'=>$request
            ] ) );
        }

        return $conn;
    }

    public function createPort( $port ) {
        $pport = new Port();
        $pport->setPort( ucfirst( ( str_replace( 'port-', '', $port['port'] ) ) ) );

        foreach ( $port['properties'] as $prop ) {
            $portType = $prop['portType'];
            $value = $prop['value'];
            $pport->addProperty( $portType, $value );
        }

        return $pport;
    }

    public function find( $researchIndex, $userId ) {
        $curl = curl_init( $this->rdsURL . '/user/' . $userId . '/research/' . $researchIndex );
        curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );
        $result = curl_exec( $curl );
        $response = json_decode( $result, true );
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

        $portIn = [];
        foreach ( $response['portIn'] as $port ) {
            $portIn[] = $this->createPort( $port );
        }

        $portOut = [];
        foreach ( $response['portIn'] as $port ) {
            $portOut[] = $this->createPort( ( $port ) );
        }

        $conn = new Research();
        $conn->setUserId( $response['userId'] );
        $conn->setStatus( $response['status'] );
        $conn->setResearchId( $response['researchId'] );
        $conn->setResearchIndex( $response['researchIndex'] );
        $conn->setportIn( $portIn );
        $conn->setportOut( $portOut );

        return $conn;
    }

    public function findAll( $userId ) {
        $curl = curl_init( $this->rdsURL . '/user/' . $userId );
        curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );
        $result = curl_exec( $curl );
        $response = json_decode( $result, true );
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

        $result = [];

        foreach ( $response as $rdsConn ) {
            $conn = new Research();
            $conn->setUserId( $rdsConn['userId'] );
            $conn->setStatus( $rdsConn['status'] );
            $conn->setResearchId( $rdsConn['researchId'] );
            $conn->setResearchIndex( $rdsConn['researchIndex'] );
            $conn->setportIn( $rdsConn['portIn'] );
            $conn->setportOut( $rdsConn['portOut'] );

            $result[] = $conn;
        }

        return $result;
    }

}
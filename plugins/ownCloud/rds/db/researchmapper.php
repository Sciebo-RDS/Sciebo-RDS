<?php
namespace OCA\RDS\Db;

use \OCA\RDS\Db\Port;
use \OCA\RDS\Db\Research;
use \OCA\RDS\Service\NotFoundException;

class ResearchMapper {
    private $rdsURL = 'https://sciebords-dev.uni-muenster.de/research';

    public function __construct() {

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
        $conn->setPortIn( $response['portIn'] );
        $conn->setPortOut( $response['portOut'] );

        return $conn;
    }

    public function update( $conn ) {
        /*$curl = curl_init( $this->rdsURL . '/user/' . $conn->getUserId() . '/research/' . $conn->getResearchIndex() );
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => 'PUT'];
        curl_setopt_array( $curl, $options );
        curl_setopt( $curl, CURLOPT_POSTFIELDS, json_encode( $conn->jsonSerialize() ) );
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
        */
        $current = $this->find( $conn->researchIndex, $conn->userId );

        return $this->updateResearch( $current, $conn );
    }

    private function updateResearch( $currentResearch, $newResearch ) {
        if ( $currentResearch->getStatus() != $newResearch->getStatus() ) {
            $newResearch->setStatus( $this->nextStatus() );
        }

        $this->removeDistinctPorts( $currentResearch, $currentResearch->getPortsIn(), $newResearch->getPortsIn() );
        $this->removeDistinctPorts( $currentResearch, $currentResearch->getPortsOut(), $newResearch->getPortsOut() );

        $this->addDistinctPorts( $currentResearch, $newResearch->getPortsIn(), $currentResearch->getPortsIn() );
        $this->addDistinctPorts( $currentResearch, $newResearch->getPortsOut(), $currentResearch->getPortsOut() );

        return $newResearch;
    }

    /**
    * Removes all $currentPorts from $conn, which are not in $newPorts
    * or has different properties as defined in $newPorts.
    * Returns TRUE, if something was removed, otherwise FALSE.
    *
    * @param \OCA\RDS\Db\Research $conn
    * @param array( \OCA\RDS\Db\Port ) $currentPorts
    * @param array( \OCA\RDS\Db\Port ) $newPorts
    * @return boolean
    */

    private function removeDistinctPorts( $conn, $currentPorts, $newPorts ) {
        $removeSth = False;

        $removeIndices = $this->getNotEqualPortIndices( $currentPorts, $newPorts );
        if ( count( $removeIndices ) > 0 ) {
            foreach ( array_reverse( $removeIndices ) as $index ) {
                $this->removePort( $conn, $index );
                $removeSth = TRUE;
            }
        }

        return $removeSth;
    }

    /**
    * Adds all $currentPorts from $conn, which are not in $newPorts
    * or has different properties as defined in $newPorts
    * Returns TRUE, if something was added, otherwise FALSE.
    *
    * @param \OCA\RDS\Db\Research $conn
    * @param array( \OCA\RDS\Db\Port ) $currentPorts
    * @param array( \OCA\RDS\Db\Port ) $newPorts
    * @return boolean
    */

    private function addDistinctPorts( $conn, $currentPorts, $newPorts ) {
        $addIndices = $this->getNotEqualPortIndices( $currentPorts, $newPorts );
        if ( count( $addIndices ) > 0 ) {
            foreach ( array_reverse( $addIndices ) as $index ) {
                $this->addPort( $conn, $currentPorts[$index] );
            }
        }
    }

    private function getNotEqualPortIndices( $currentPorts, $newPorts ) {
        $returnList = [];
        $index = 0;

        foreach ( $currentPorts as $i ) {
            $found = FALSE;
            foreach ( $newPorts as $j ) {
                if ( $i->getPort() == $j->getPort() ) {
                    if ( ! $i->propertiesEqual( $j ) ) {
                        $returnList[] = $index;
                    }
                    $found = TRUE;
                }
            }

            if ( !$found ) {
                $returnList[] = $index;
            }

            $index++;
        }

        return $returnList;
    }

    private function nextStatus( $conn ) {
        $url = $this->rdsURL . '/user/' . $userId . '/research/' . $researchIndex . '/status';
        throw new Exception( 'Not implemented' );

        return 0;
    }

    private function addPort( $conn, $port ) {
        
    }

    private function removePort( $conn, $index ) {
        
    }

    private function removePortIn( $researchIndex, $userId, $port ) {
        return internalRemovePort( $conn, 'imports' );
    }

    private function removePortOut( $researchIndex, $userId, $port ) {
        return internalRemovePort( $conn, 'exports' );
    }

    private function addPortIn( $researchIndex, $userId, $port ) {
        return internalAddPort( $researchIndex, $userId, $port, 'imports' );
    }

    private function addPortOut( $researchIndex, $userId, $port ) {
        return internalAddPort( $researchIndex, $userId, $port, 'exports' );
    }

    private function internalRemovePort( $researchIndex, $userId, $portIndex, $where ) {
        # TODO: implements me
        $url = $this->rdsURL . '/user/' . $userId . '/research/' . $researchIndex . '/' . $where.'/'.$portIndex;
        throw new Exception( 'Not implemented' );
    }

    private function internalAddPort( $researchIndex, $userId, $port, $where ) {
        # TODO: implements me
        $url = $this->rdsURL . '/user/' . $userId . '/research/' . $researchIndex . '/' . $where;
        throw new Exception( 'Not implemented' );
    }

    private function setStatus( $conn ) {
        # TODO: implements me
        $url = $this->rdsURL . '/user/' . $userId . '/research/' . $researchIndex . '/status';
        throw new Exception( 'Not implemented' );
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
        $pport->setId( $portIn['id'] );
        $pport->setPort( $portIn['port'] );

        foreach ( $portIn as $prop ) {
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

        $portIn = $this->createPort( $response['portIn'] );
        $portOut = $this->createPort( $response['portOut'] );

        $conn = new Research();
        $conn->setUserId( $response['userId'] );
        $conn->setStatus( $response['status'] );
        $conn->setResearchId( $response['researchId'] );
        $conn->setResearchIndex( $response['researchIndex'] );
        $conn->addImport( $portIn );
        $conn->addExport( $portOut );

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
            $conn->setPortIn( $rdsConn['portIn'] );
            $conn->setPortOut( $rdsConn['portOut'] );

            $result[] = $conn;
        }

        return $result;
    }

}
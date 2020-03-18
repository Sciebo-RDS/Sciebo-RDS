<?php
# a lot of this was taken from https://github.com/owncloud/app-tutorial/blob/master/service/noteservice.php

namespace OCA\RDS\Service;

use Exception;

use OCP\AppFramework\Db\DoesNotExistException;
use OCP\AppFramework\Db\MultipleObjectsReturnedException;

use OCA\RDS\Db\Connection;
use OCA\RDS\Db\ConnectionMapper;

class ConnectionService {
    private $mapper;

    public function __construct( ConnectionMapper $mapper ) {
        $this->mapper = $mapper;
    }

    public function findAll( $userId ) {
        return $this->mapper->findAll( $userId );
    }

    private function handleException ( $e ) {
        if ( $e instanceof DoesNotExistException ||
        $e instanceof MultipleObjectsReturnedException ) {
            throw new NotFoundException( $e->getMessage() );
        } else {
            throw $e;
        }
    }

    public function find( $projectIndex, $userId ) {
        try {
            return $this->mapper->find( $projectIndex, $userId );
        } catch( Exception $e ) {
            $this->handleException( $e );
        }
    }

    public function create( $userId ) {
        $conn = $this->mapper->insert( $userId );
        return $conn;
    }

    public function update( $userId, $projectIndex, $portIn, $portOut, $status ) {
        try {
            $conn = new Connection();
            $conn->setUserId( $userId );
            $conn->setProjectIndex( $projectIndex );
            $conn->setPortIn( $portIn );
            $conn->setPortOut( $portOut );
            $conn->setStatus( $status );

            return $this->mapper->update( $conn );
        } catch ( Exception $e ) {
            $this->handleException( $e );
        }
    }

    public function delete( $projectIndex, $userId ) {
        try {
            $conn = $this->mapper->find( $projectIndex, $userId );
            $this->mapper->delete( $conn );
            return $conn;
        } catch( Exception $e ) {
            $this->handleException( $e );
        }
    }
}
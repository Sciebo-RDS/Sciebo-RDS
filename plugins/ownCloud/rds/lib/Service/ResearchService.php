<?php
# a lot of this was taken from https://github.com/owncloud/app-tutorial/blob/master/service/noteservice.php

namespace OCA\RDS\Service;

use Exception;

use OCP\AppFramework\Db\DoesNotExistException;
use OCP\AppFramework\Db\MultipleObjectsReturnedException;

use \OCA\RDS\Db\Port;
use \OCA\RDS\Db\Research;
use \OCA\RDS\Db\ResearchMapper;

class ResearchService {
    private $mapper;

    public function __construct( ResearchMapper $mapper ) {
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

    public function find( $researchIndex, $userId ) {
        try {
            return $this->mapper->find( $researchIndex, $userId );
        } catch( Exception $e ) {
            $this->handleException( $e );
        }
    }

    public function create( $userId ) {
        try {
            $conn = $this->mapper->insert( $userId );
            return $conn;
        } catch( Exception $e ) {
            $this->handleException( $e );
        }
    }

    public function update( $userId, $researchIndex, $portsIn, $portsOut, $status ) {
        try {
            $pportsIn = $this->mapper->createPort( $portsIn );
            $pportsOut = $this->mapper->createPort( $portsOut );

            $conn = new Research();
            $conn->setUserId( $userId );
            $conn->setResearchIndex( $researchIndex );
            $conn->addImport( $pportsIn );
            $conn->addExport( $pportsOut );
            $conn->setStatus( $status );

            return $this->mapper->update( $conn );
        } catch ( Exception $e ) {
            $this->handleException( $e );
        }
    }

    public function delete( $researchIndex, $userId ) {
        try {
            return $this->mapper->delete( $researchIndex, $userId );
        } catch( Exception $e ) {
            $this->handleException( $e );
        }
    }
}
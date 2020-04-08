<?php
# a lot of this was taken from https://github.com/owncloud/app-tutorial/blob/master/service/noteservice.php

namespace OCA\RDS\Service;

use Exception;

use OCP\AppFramework\Db\DoesNotExistException;
use OCP\AppFramework\Db\MultipleObjectsReturnedException;

use OCA\RDS\Db\Metadata;
use OCA\RDS\Db\MetadataMapper;

class MetadataService {
    private $mapper;

    public function __construct( MetadataMapper $mapper ) {
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

    public function find( $researchId, $port ) {
        try {
            return $this->mapper->find( $researchId, $port );
        } catch( Exception $e ) {
            $this->handleException( $e );
        }
    }

    public function update( $researchId, $metadataDict ) {
        try {
            return $this->mapper->update( $metadataDict );
        } catch ( Exception $e ) {
            $this->handleException( $e );
        }
    }
}
<?php
# a lot of this was taken from https://github.com/owncloud/app-tutorial/blob/master/service/noteservice.php

namespace OCA\RDS\Service;

use Exception;

use OCP\AppFramework\Db\DoesNotExistException;
use OCP\AppFramework\Db\MultipleObjectsReturnedException;

use \OCA\RDS\Db\Service;
use \OCA\RDS\Db\ServiceMapper;

class ServiceportService {
    private $mapper;

    public function __construct( ServiceMapper $mapper ) {
        $this->mapper = $mapper;
    }

    public function findAll() {
        try {
            return $this->mapper->findAll();
        } catch( Exception $e ) {
            $this->handleException( $e );
        }
    }

    private function handleException ( $e ) {
        if ( $e instanceof DoesNotExistException ||
        $e instanceof MultipleObjectsReturnedException ) {
            throw new NotFoundException( $e->getMessage() );
        } else {
            throw $e;
        }
    }

    public function find( $servicename ) {
        try {
            return $this->mapper->find( $servicename );
        } catch( Exception $e ) {
            $this->handleException( $e );
        }
    }
}
<?php
# a lot of this was taken from https://github.com/owncloud/app-tutorial/blob/master/service/noteservice.php

namespace OCA\RDS\Service;

use Exception;

use OCP\AppFramework\Db\DoesNotExistException;
use OCP\AppFramework\Db\MultipleObjectsReturnedException;

use \OCA\RDS\Db\Service;
use \OCA\RDS\Db\UserserviceMapper;

class UserserviceportService {
    private $mapper;


    public function __construct( UserserviceMapper $mapper ) {
        $this->mapper = $mapper;
    }

    public function findAll( $userId ) {
        try {
            return $this->mapper->findAll( $userId );
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

    public function find( $servicename, $userId ) {
        try {
            return $this->mapper->find( $servicename, $userId );
        } catch( Exception $e ) {
            $this->handleException( $e );
        }
    }

    public function create( $userId, $servicename, $oauthtoken, $refreshtoken, $expirationDate ) {
        $service = $this->mapper->insert( $userId, $servicename, $oauthtoken, $refreshtoken, $expirationDate );
        return $service;
    }

    public function delete( $servicename, $userId ) {
        try {
            return $this->mapper->delete( $servicename, $userId );
        } catch( Exception $e ) {
            $this->handleException( $e );
        }
    }

    public function register($servicename, $code, $state, $userId, $secret) {
        try {
            return $this->mapper->register( $servicename, $code, $state, $userId, $secret );
        } catch( Exception $e ) {
            $this->handleException( $e );
        }
    }
}
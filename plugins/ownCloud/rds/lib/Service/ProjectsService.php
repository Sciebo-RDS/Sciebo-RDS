<?php
# a lot of this was taken from https://github.com/owncloud/app-tutorial/blob/master/service/noteservice.php

namespace OCA\RDS\Service;

use Exception;

use OCP\AppFramework\Db\DoesNotExistException;
use OCP\AppFramework\Db\MultipleObjectsReturnedException;

use \OCA\RDS\Db\Project;
use \OCA\RDS\Db\ProjectsMapper;

class ProjectsService {
    private $mapper;

    public function __construct( ProjectsMapper $mapper ) {
        $this->mapper = $mapper;
    }

    public function findAll( $userId, $servicename ) {
        return $this->mapper->findAll( $userId, $servicename );
    }

    private function handleException ( $e ) {
        if ( $e instanceof DoesNotExistException ||
        $e instanceof MultipleObjectsReturnedException ) {
            throw new NotFoundException( $e->getMessage() );
        } else {
            throw $e;
        }
    }

    public function find( $userId, $servicename, $projectId ) {
        try {
            return $this->mapper->find( $userId, $servicename, $projectId );
        } catch( Exception $e ) {
            $this->handleException( $e );
        }
    }

    public function insert( $userId, $servicename ) {
        try {
            return $this->mapper->insert( $userId, $servicename );
        } catch ( Exception $e ) {
            $this->handleException( $e );
        }
    }

    public function destroy( $userId, $servicename, $projectId ) {
        try {
            return $this->mapper->delete( $userId, $servicename, $projectId );
        } catch ( Exception $e ) {
            $this->handleException( $e );
        }
    }
}
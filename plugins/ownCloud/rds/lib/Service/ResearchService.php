<?php
# a lot of this was taken from https://github.com/owncloud/app-tutorial/blob/master/service/noteservice.php

namespace OCA\RDS\Service;

use Exception;

use OCP\AppFramework\Db\DoesNotExistException;
use OCP\AppFramework\Db\MultipleObjectsReturnedException;
use OCP\ILogger;

use \OCA\RDS\Db\Port;
use \OCA\RDS\Db\Research;
use \OCA\RDS\Db\ResearchMapper;

class ResearchService {
    private $mapper;

    public function __construct( ILogger $logger, $appName, ResearchMapper $mapper ) {
        $this->mapper = $mapper;
        $this->appName = $appName;
        $this->logger = $logger;
    }

    public function log( $message, $arr ) {
        $this->logger->error( $message, array_merge( ['app' => $this->appName], $arr ) );
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

    public function update( $userId, $researchIndex, $portIn, $portOut, $status ) {
        try {
            $conn = new Research();
            $conn->setUserId( $userId );
            $conn->setResearchIndex( $researchIndex );

            foreach ( $portIn as $port ) {
                $pportIn = $this->mapper->createPort( $port );
                $conn->addImport( $pportIn );
            }

            foreach ( $portOut as $port ) {
                $pportOut = $this->mapper->createPort( $port );
                $conn->addExport( $pportOut );
            }

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

    public function files( $userId ) {
        try {
            $allResearch = $this->mapper->findAll( $userId );
            $folders = [];

            foreach ( $allResearch as $research ) {
                foreach ( array_merge( $research->getPortIn(), $research->getPortOut() ) as $port ) {
                    foreach ( $port['properties'] as $prop ) {
                        if ( $prop['portType'] == 'customProperties' ) {
                            foreach ( $prop['value'] as $val ) {
                                if ( $val['key'] == 'filepath' ) {
                                    $folders[] = $val['value'];
                                }
                            }
                        }
                    }
                }
            }

            return $folders;
        } catch( Exception $e ) {
            $this->handleException( $e );
        }
    }

    public function updateFiles( $userId, $researchId, $force = null ) {
        try {
            // TODO: execute exporter in RDS, force removes all files and add them anew
        } catch( Exception $e ) {
            $this->handleException( $e );
        }
    }
}
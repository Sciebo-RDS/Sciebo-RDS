<?php
# a lot of this was taken from https://github.com/owncloud/app-tutorial/blob/master/service/noteservice.php

namespace OCA\RDS\Service;

use Exception;

use OCP\AppFramework\Db\DoesNotExistException;
use OCP\AppFramework\Db\MultipleObjectsReturnedException;

use \OCA\RDS\Db\Metadata;
use \OCA\RDS\Db\MetadataMapper;

class MetadataService
{
    private $mapper;

    public function __construct(MetadataMapper $mapper)
    {
        $this->mapper = $mapper;
    }

    public function findAll($userId, $researchIndex)
    {
        return $this->mapper->findAll($userId, $researchIndex);
    }

    private function handleException($e)
    {
        if (
            $e instanceof DoesNotExistException ||
            $e instanceof MultipleObjectsReturnedException
        ) {
            throw new NotFoundException($e->getMessage());
        } else {
            throw $e;
        }
    }

    public function find($userId, $researchIndex, $port)
    {
        try {
            return $this->mapper->find($userId, $researchIndex, $port);
        } catch (Exception $e) {
            $this->handleException($e);
        }
    }

    public function update($userId, $researchIndex, $metadataDict)
    {
        try {
            $md = new Metadata();
            $md->setUserId($userId);
            $md->setResearchIndex($researchIndex);
            $md->setMetadata($metadataDict);

            return $this->mapper->update($md);
        } catch (Exception $e) {
            $this->handleException($e);
        }
    }

    public function jsonschema()
    {
        try {
            return $this->mapper->jsonschema();
        } catch (Exception $e) {
            $this->handleException($e);
        }
    }
}

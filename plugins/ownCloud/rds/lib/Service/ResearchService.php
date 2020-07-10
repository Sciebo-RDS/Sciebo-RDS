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

class ResearchService
{
    private $mapper;

    public function __construct(ILogger $logger, $appName, ResearchMapper $mapper)
    {
        $this->mapper = $mapper;
        $this->appName = $appName;
        $this->logger = $logger;
    }

    public function log($message, $arr)
    {
        $this->logger->error($message, array_merge(['app' => $this->appName], $arr));
    }

    public function findAll($userId)
    {
        return $this->mapper->findAll($userId);
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

    public function find($researchIndex, $userId)
    {
        try {
            return $this->mapper->find($researchIndex, $userId);
        } catch (Exception $e) {
            $this->handleException($e);
        }
    }

    public function create($userId)
    {
        try {
            $conn = $this->mapper->insert($userId);
            return $conn;
        } catch (Exception $e) {
            $this->handleException($e);
        }
    }

    public function update($userId, $researchIndex, $portIn, $portOut, $status)
    {
        try {
            $conn = new Research();
            $conn->setUserId($userId);
            $conn->setResearchIndex($researchIndex);

            foreach ($portIn as $port) {
                $pportIn = $this->mapper->createPort($port);
                $conn->addImport($pportIn);
            }

            foreach ($portOut as $port) {
                $pportOut = $this->mapper->createPort($port);
                $conn->addExport($pportOut);
            }

            $conn->setStatus($status);

            return $this->mapper->update($conn);
        } catch (Exception $e) {
            $this->handleException($e);
        }
    }

    public function delete($researchIndex, $userId)
    {
        try {
            return $this->mapper->delete($researchIndex, $userId);
        } catch (Exception $e) {
            $this->handleException($e);
        }
    }

    public function files($userId, $id = null)
    {
        try {
            $folders = $this->getFolders($userId);
            $ret = [];
            foreach ($folders as $folder) {
                if ($id != null && $id == $folder['researchIndex']) {
                    return $folder;
                }
                $ret[] = $folder['path'];
            }

            return $ret;
        } catch (Exception $e) {
            $this->handleException($e);
        }
    }

    private function getFolders($userId)
    {
        $allResearch = $this->mapper->findAll($userId);
        $folders = [];

        foreach ($allResearch as $research) {
            if ($research->getStatus() == 4) {
                continue;
            }
            foreach (array_merge($research->getPortIn(), $research->getPortOut()) as $port) {
                foreach ($port['properties'] as $prop) {
                    if ($prop['portType'] == 'customProperties') {
                        foreach ($prop['value'] as $val) {
                            if ($val['key'] == 'filepath') {
                                $folders[] = [
                                    'path' => $val['value'],
                                    'researchIndex' => $research->getResearchIndex()
                                ];
                            }
                        }
                    }
                }
            }
        }
        return $folders;
    }

    public function updateFiles($userId, $id = null, $filename = null)
    {
        function startsWith($string, $startString)
        {
            $len = strlen($startString);
            return (substr($string, 0, $len) === $startString);
        }

        try {
            if ($id == null && $filename == null) {
                throw new Exception('no researchIndex or filename were given');
            }

            $found = false;
            if ($filename != null && $id == null) {
                $folders = $this->getFolders($userId);
                foreach ($folders as $folder) {
                    if (startsWith($filename, $folder['path'])) {
                        $found = true;
                        $id = $folder['researchIndex'];
                        $settings = $this->getSettings($userId, $id);
                        break;
                    }
                }
            } else {
                $found = true;
            }

            if (!$found) {
                return false;
            }

            $settings = $this->getSettings($userId, $id);

            if ($filename != null) {
                // TODO: trigger export for specific file in research for userId and researchIndex
            }
            return $this->mapper->triggerExport($userId, $id);
        } catch (Exception $e) {
            $this->handleException($e);
        }
    }

    public function getSettings($userId, $researchIndex)
    {
        // TODO: get settings from owncloud or rds
        return [];
    }

    public function updateSettings($userId, $researchIndex)
    {
        // TODO: set settings from owncloud or rds
        return [];
    }

    public function publish($userId, $researchIndex)
    {
        return $this->mapper->publish($userId, $researchIndex);
    }

    public function deleteUser($userId)
    {
        return $this->mapper->deleteUser($userId);
    }
}

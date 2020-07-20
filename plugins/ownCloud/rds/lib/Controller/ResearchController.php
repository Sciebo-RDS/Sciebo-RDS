<?php

namespace OCA\RDS\Controller;

use OCP\ILogger;
use OCP\IRequest;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http;
use OCP\AppFramework\Http\JSONResponse;
use \OCA\RDS\Service\ResearchService;


class ResearchController extends Controller
{
    private $userId;
    private $service;

    use Errors;

    public function __construct(ILogger $logger, $AppName, IRequest $request, ResearchService $service, $userId)
    {
        parent::__construct($AppName, $request);
        $this->logger = $logger;
        $this->userId = $userId;
        $this->service = $service;
    }

    public function log($message, $arr)
    {
        $this->logger->error($message, array_merge(['app' => $this->appName], $arr));
    }

    /**
     * Returns all research in rds for userId
     *
     * @param integer $id
     * @return string returns json
     * 
     * @NoCSRFRequired
     * @NoAdminRequired
     */
    public function index()
    {
        return $this->handleNotFound(function () {
            return $this->service->findAll($this->userId);
        });
    }

    /**
     * Returns all Research informations in rds for given id
     *
     * @param integer $id
     * @return string returns json
     *
     * @NoAdminRequired
     */
    public function show($id)
    {
        return $this->handleNotFound(function () use ($id) {
            return $this->service->find($id, $this->userId);
        });
    }

    /**
     * Create a new Research.
     *
     * @return string returns the Research object as json
     * 
     * @NoAdminRequired
     */
    public function create()
    {
        return $this->handleNotFound(function () {
            return $this->service->create($this->userId);
        });
    }

    /**
     * Update a single Research in rds system
     *
     * @param integer $researchIndex
     * @param integer $status
     * @param array $portIn
     * @param array $portOut
     * @return string returns the updated object as json
     * 
     * @NoAdminRequired
     */
    public function update($id, $status, $portIn, $portOut)
    {
        return $this->handleNotFound(function () use ($id, $status, $portIn, $portOut) {
            return $this->service->update($this->userId, $id, $portIn, $portOut, $status);
        });
    }

    /**
     * Removes a single research from the user in RDS.
     *
     * @param integer $id
     * @return string returns the removed object as json
     *
     * @NoAdminRequired
     */
    public function destroy($id)
    {
        return $this->handleNotFound(function () use ($id) {
            return $this->service->delete($id, $this->userId);
        });
    }

    /**
     * Returns all folders in all studies.
     * 
     * @NoAdminRequired
     */
    public function filesIndex()
    {
        return $this->handleNotFound(function () {
            return $this->service->files($this->userId);
        });
    }

    /**
     * Returns all filepaths for given research.
     * 
     * @param integer $id have to be a researchIndex
     * @return array returns an assoc array
     * 
     * @NoAdminRequired
     */
    public function filesGet($id)
    {
        return $this->handleNotFound(function () use ($id) {
            return $this->service->files($this->userId, $id);
        });
    }


    /**
     * Trigger an update request for research project to exporter func in RDS
     * 
     * @return boolean True, if Trigger was successful. False otherwise.
     * @NoAdminRequired
     */
    public function filesTrigger($id, $filename = null)
    {
        return $this->handleNotFound(function () use ($id, $filename) {
            return $this->service->updateFiles($this->userId, $id, $filename);
        });
    }

    /**
     * Trigger an update request for given filename to exporter func in RDS
     * 
     * @return boolean True, if Trigger was successful. False otherwise.
     * @NoAdminRequired
     */
    public function filesIndexUpload($filename)
    {
        return $this->handleNotFound(function () use ($filename) {
            return $this->service->updateFiles($this->userId, null, $filename);
        });
    }

    /**
     * Returns all settings for rds exporter.
     * 
     * @param integer $id have to be a researchIndex
     * @return array returns an assoc array
     * 
     * @NoAdminRequired
     */
    public function filesSettingsGet($id)
    {
        return $this->handleNotFound(function () use ($id) {
            return $this->service->getSettings($this->userId, $id);
        });
    }

    /**
     * Updates the settings for rds exporter.
     * 
     * @param integer $id have to be a researchIndex
     * @param array $settings have to be an assoc array
     * @return array returns an assoc array
     * 
     * @NoAdminRequired
     */
    public function filesSettingsUpdate($id, $settings)
    {
        return $this->handleNotFound(function () use ($id, $settings) {
            return $this->service->updateSettings($this->userId, $id, $settings);
        });
    }

    /**
     * Publish / Closes the given id in rds.
     * 
     * @param integer $id have to be a researchIndex
     * 
     * @NoAdminRequired
     */
    public function publish($id)
    {
        return $this->handleNotFound(function () use ($id) {
            return $this->service->publish($this->userId, $id);
        });
    }

    /**
     * Remove the current user in rds.
     * 
     * @NoAdminRequired
     */
    public function deleteUser()
    {
        return $this->handleNotFound(function () {
            return $this->service->deleteUser($this->userId);
        });
    }
}

<?php

namespace OCA\RDS\Controller;

use OCP\IRequest;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http;
use OCP\AppFramework\Http\JSONResponse;
use OCA\RDS\Service\ConnectionService;


class ConnectionController extends Controller
{
    private $userId;
    private $service;
    
    public function __construct($AppName, IRequest $request, ConnectionService $service, $userId)
    {
        parent::__construct($AppName, $request);
        $this->userId = $userId;
        $this->service = $service;
    }

    /**
     * Returns all connections in rds for userId
     *
     * @param integer $id
     * @return string returns json
     * 
     * @NoAdminRequired
     */
    public function index() {
        return new JSONResponse($this->service->findAll($this->userId));
    }

    /**
     * Returns all connection informations in rds for given id
     *
     * @param integer $id
     * @return string returns json
     *
     * @NoCSRFRequired
     * @NoAdminRequired
     */
    public function show($id) {
        return $this->handleNotFound(function () use ($id) {
            return new JSONResponse($this->service->find($id, $this->userId));
        });
    }

    /**
     * Create a new connection.
     *
     * @return string returns the connection object as json
     * 
     * @NoAdminRequired
     */
    public function create() {
        return new JSONResponse($this->service->create($this->userId));
    }

    /**
     * Update a single connection in rds system
     *
     * @param integer $projectIndex
     * @param array $portIn
     * @param array $portOut
     * @param integer $status
     * @return string returns the updated object as json
     *
     * @NoAdminRequired
     */
    public function update($projectIndex, $portIn, $portOut, $status) {
        return new JSONResponse($this->service->update( $this->userId, $projectIndex, $portIn, $portOut, $status));
    }

    /**
     * Removes a single connection from the user in RDS.
     *
     * @param integer $projectIndex
     * @return string returns the removed object as json
     *
     * @NoAdminRequired
     */
    public function remove($projectIndex) {
        return new JSONResponse($this->service->remove($projectIndex, $this->userId));
    }
}

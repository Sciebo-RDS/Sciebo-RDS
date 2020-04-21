<?php

namespace OCA\RDS\Controller;

use OCP\IRequest;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http;
use OCP\AppFramework\Http\JSONResponse;
use \OCA\RDS\Service\MetadataService;


class MetadataController extends Controller
{
    private $userId;
    private $service;
    
    use Errors;
    
    public function __construct($AppName, IRequest $request, MetadataService $service, $userId)
    {
        parent::__construct($AppName, $request);
        $this->userId = $userId;
        $this->service = $service;
    }

    /**
     * Returns all metadata for id
     *
     * @param integer $id
     * @return string returns json
     * 
     * @NoAdminRequired
     * @NoCSRFRequired
     */
    public function index() {
        return $this->handleNotFound(function () {
            return new JSONResponse($this->service->findAll($his->$userId));
        });
    }

    /**
     * Returns metadata for resarchId in given port
     *
     * @param integer $id
     * @param string $port
     * @return string returns json
     *
     * @NoCSRFRequired
     * @NoAdminRequired
     */
    public function show($id, $port) {
        if(empty($port)){
            return $this->handleNotFound(function () use ($id) {
                return new JSONResponse($this->service->findAll($id));
            });
        }
        return $this->handleNotFound(function () use ($id, $port) {
            return new JSONResponse($this->service->find($id, $port));
        });
    }

    /**
     * Update a single Research in rds system
     *
     * @param integer $id
     * @param array $metadataArr
     * @return string returns the updated object as json
     *
     * @NoAdminRequired
     */
    public function update($id, $metadataArr) {
        return new JSONResponse($this->service->update( $id, $metadataArr ));
    }

    /**
     * Returns the current used jsonschema in rds system for metadata
     *
     * @return string returns the jsonschema
     *
     * @NoCSRFRequired
     * @NoAdminRequired
     */
    public function jsonschema() {
        return new JSONResponse($this->service->jsonschema());
    }

}

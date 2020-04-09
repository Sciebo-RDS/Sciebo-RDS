<?php

namespace OCA\RDS\Controller;

use OCP\IRequest;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http;
use OCP\AppFramework\Http\JSONResponse;
use OCA\RDS\Service\MetadataService;


class MetadataController extends Controller
{
    private $userId;
    private $service;
    
    public function __construct($AppName, IRequest $request, MetadataService $service, $userId)
    {
        parent::__construct($AppName, $request);
        $this->userId = $userId;
        $this->service = $service;
    }

    /**
     * Returns all metadata for researchId
     *
     * @param integer $researchId
     * @return string returns json
     * 
     * @NoAdminRequired
     * @NoCSRFRequired
     */
    public function index($researchId) {
        return new JSONResponse($this->service->findAll($researchId));
    }

    /**
     * Returns metadata for resarchId in given port
     *
     * @param integer $researchId
     * @param string $port
     * @return string returns json
     *
     * @NoCSRFRequired
     * @NoAdminRequired
     */
    public function show($researchId, $port) {
        return $this->handleNotFound(function () use ($researchId) {
            return new JSONResponse($this->service->find($researchId, $port));
        });
    }

    /**
     * Update a single Research in rds system
     *
     * @param integer $researchId
     * @param array $metadataArr
     * @return string returns the updated object as json
     *
     * @NoAdminRequired
     */
    public function update($researchId, $metadataArr) {
        return new JSONResponse($this->service->update( $researchId, $metadataArr ));
    }

    /**
     * Returns the current used jsonschema in rds system for metadata
     *
     * @return string returns the jsonschema
     *
     * @NoAdminRequired
     */
    public function jsonschema() {
        return new JSONResponse($this->service->jsonschema());
    }

}

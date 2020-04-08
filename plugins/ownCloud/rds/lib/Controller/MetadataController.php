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
     * @param integer $id
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
     * @param integer $id
     * @param string $port
     * @return string returns json
     *
     * @NoCSRFRequired
     * @NoAdminRequired
     */
    public function show($id, $port) {
        return $this->handleNotFound(function () use ($id) {
            return new JSONResponse($this->service->find($id, $port));
        });
    }

    /**
     * Update a single Research in rds system
     *
     * @param integer $researchId
     * @param array $metadataDict
     * @return string returns the updated object as json
     *
     * @NoAdminRequired
     */
    public function update($researchId, $metadataDict) {
        return new JSONResponse($this->service->update( $researchId, $metadataDict ));
    }

}

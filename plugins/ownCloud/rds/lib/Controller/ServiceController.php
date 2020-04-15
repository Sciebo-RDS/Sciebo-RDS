<?php

namespace OCA\RDS\Controller;

use OCP\IRequest;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http;
use OCP\AppFramework\Http\JSONResponse;
use \OCA\RDS\Service\ServiceportService;
use OCP\AppFramework\Http\RedirectResponse;

class ServiceController extends Controller {
    private $service;

    use Errors;


    public function __construct( $AppName, IRequest $request, ServiceportService $service ) {
        parent::__construct( $AppName, $request );
        $this->service = $service;
    }

    /**
    * Returns a list with all services from RDS.
    *
    * @return array a list with object with key 'jwt', see $this->show()
    *
    * @NoAdminRequired
    * @NoCSRFRequired
    */

    public function index() {
        return $this->handleNotFound(function () {
            return $this->service->findAll();
        });
    }

    /**
    * Returns a single service from RDS to authenticate with.
    *
    * @param string $id
    * @return object an object with jwt encoded object with keys
    * 'id', 'authorize_url', 'date'
    *
    * @NoAdminRequired
    * @NoCSRFRequired
    */

    public function show( $id ) {
        return $this->handleNotFound(function () use ($id) {
            return $this->service->find($id);
        });
    }
}

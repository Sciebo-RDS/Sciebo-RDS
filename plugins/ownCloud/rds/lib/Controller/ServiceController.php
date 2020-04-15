<?php

namespace OCA\RDS\Controller;

use OCP\IRequest;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http;
use OCP\AppFramework\Http\JSONResponse;
use \OCA\RDS\Service\ServiceportService;
use OCP\AppFramework\Http\RedirectResponse;

class ServiceController extends Controller {
    private $userId;
    private $service;

    use Errors;

    public function __construct( $AppName, IRequest $request, ServiceportService $service, $userId ) {
        parent::__construct( $AppName, $request );
        $this->userId = $userId;
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
        return new JSONResponse( $this->service->index() );
    }

    /**
    * Returns a single service from RDS to authenticate with.
    *
    * @param string $servicename
    * @return object an object with jwt encoded object with keys
    * 'servicename', 'authorize_url', 'date'
    *
    * @NoAdminRequired
    * @NoCSRFRequired
    */

    public function show( $servicename ) {
        return $this->handleNotFound(function () use ($servicename) {
            return new JSONResponse($this->service->find($servicename, $this->userId));
        });
    }

    /**
    * Removes a single service from the user in RDS.
    *
    * @param string $servicename
    * @return bool returns true for success, else false
    *
    * @NoAdminRequired
    */

    public function delete( $servicename ) {
        return $this->handleNotFound(function () use ($servicename) {
             new JSONResponse( $this->service->delete( $servicename, $this->userId ) );
             return new RedirectResponse('index.php/settings/personal?sectionid=additional');
        });
    }

    /**
    * Returns a list with all services from rds, which registered for user.
    *
    * @return string a list of strings, which are servicenames
    *
    * @NoAdminRequired
    * @NoCSRFRequired
    */

    public function getRegisteredServicesForUser() {
        return new JSONResponse( $this->service->findAll( $this->userId ) );
    }
}

<?php

namespace OCA\RDS\Controller;

use OCP\AppFramework\ {
    Controller,
    Http\TemplateResponse
}
;

use OCP\IRequest;
use OCP\Template;
use \OCA\OAuth2\Db\Client;
use \OCA\OAuth2\Db\ClientMapper;
use \OCA\RDS\Service\UserserviceportService;

/**
- Define a new page controller
*/

class PageController extends Controller {
    /** @var ClientMapper */
    private $clientMapper;
    private $userserviceMapper;
    private $userId;
    private $rdsURL = 'http://sciebords-dev.uni-muenster.de/token-service';

    public function __construct( $AppName, IRequest $request, ClientMapper $clientMapper, UserserviceportService $userservice, $userId ) {
        parent::__construct( $AppName, $request );
        $this->clientMapper = $clientMapper;
        $this->userId = $userId;
        $this->userservice = $userservice;
    }

    /**
    * @NoCSRFRequired
    * @NoAdminRequired
    */

    public function index() {
        return $this->checkUserForRDSActivated( 'main.research' );
    }

    /**
    * Returns a list with all services from rds, which registered for user.
    *
    * @return string a list of strings, which are servicenames
    *
    * @NoAdminRequired
    */

    private function checkUserForRDSActivated( $templateIfActivated, $params = [] ) {
        $found = false;

        $service = $this->userservice->find( 'Owncloud', $this->userId );
        if ( 'Owncloud' == $service->servicename ) {
            $found = true;
        }

        if ( !$found ) {
            return new TemplateResponse( 'rds', 'not_authorized' );
        }

        return new TemplateResponse( 'rds', $templateIfActivated, $params );
    }

}

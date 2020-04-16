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
    * @NoCSRFRequired
    * @NoAdminRequired
    */

    public function researchShow( $id ) {
        return $this->checkUserForRDSActivated( 'main.research', ['id'=>$id] );
    }

    /**
    * @NoCSRFRequired
    * @NoAdminRequired
    */

    public function researchEdit( $id ) {
        return $this->checkUserForRDSActivated( 'main.research', ['id'=>$id] );
    }

    /**
    * Returns a list with all services from rds, which registered for user.
    *
    * @return string a list of strings, which are servicenames
    *
    * @NoAdminRequired
    */

    private function checkUserForRDSActivated( $templateIfActivated, $params = [] ) {
        try {
            $service = $this->userservice->find( 'Owncloud', $this->userId );
            return new TemplateResponse( 'rds', $templateIfActivated, $params );
        } catch( Exception $e ) {
            return new TemplateResponse( 'rds', 'not_authorized' );
        }
    }

}

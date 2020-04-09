<?php

namespace OCA\RDS\Controller;

use OCP\AppFramework\ {
    Controller,
    Http\TemplateResponse
}
;

use OCP\IRequest;
use OCP\Template;
use OCA\OAuth2\Db\Client;
use OCA\OAuth2\Db\ClientMapper;

/**
- Define a new page controller
*/

class PageController extends Controller {
    /** @var ClientMapper */
    private $clientMapper;
    private $userId;
    private $rdsURL = 'http://sciebords-dev.uni-muenster.de/token-service';

    public function __construct( $AppName, IRequest $request, ClientMapper $clientMapper, $userId ) {
        parent::__construct( $AppName, $request );
        $this->clientMapper = $clientMapper;
        $this->userId = $userId;
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

        $services = $this->getRegisteredServicesForUser();
        foreach ( $services as $service ) {
            if ( 'Owncloud' == $service ) {
                $found = true;
                break;
            }
        }

        if ( !$found ) {
            return new TemplateResponse( 'rds', 'not_authorized' );
        }

        return new TemplateResponse( 'rds', $templateIfActivated, $params );
    }

    public function getRegisteredServicesForUser() {
        $curl = curl_init( $this->rdsURL . '/user/' . $this->userId . '/service' );
        curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );

        $response = json_decode( curl_exec( $curl ) );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            return [];
        }

        return $response;
    }
}

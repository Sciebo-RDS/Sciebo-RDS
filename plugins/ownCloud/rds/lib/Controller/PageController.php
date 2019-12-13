<?php

namespace OCA\RDS\Controller;

use OCP\AppFramework\{
    Controller,
    Http\TemplateResponse
};

use OCP\IRequest;
use OCP\Template;
use OCA\OAuth2\Db\Client;
use OCA\OAuth2\Db\ClientMapper;

/**
 - Define a new page controller
 */
class PageController extends Controller
{
    /** @var ClientMapper */
    private $clientMapper;
    private $userId;

    public function __construct($AppName, IRequest $request, ClientMapper $clientMapper, $userId)
    {
        parent::__construct($AppName, $request);
        $this->clientMapper = $clientMapper;
        $this->userId = $userId;
    }

    /**
     * @NoCSRFRequired
     * @NoAdminRequired
     */
    public function index()
    {
        $clients = $this->clientMapper->findByUser($this->userId);
        $found = false;

        if (!empty($clients)) {
            foreach ($clients as $client) {
                if ("Sciebo RDS" == $client->getName()) {
                    $found = true;
                    break;
                }
            }
        }

        if ($found) {
            return new TemplateResponse('rds', 'main');

        } else {
            return new TemplateResponse('rds', 'not_authorized');
        }
    }
}

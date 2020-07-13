<?php

namespace OCA\RDS\Controller;

use OCP\AppFramework\{
    Controller,
    Http\TemplateResponse
};

use OCP\IRequest;
use OCP\Template;
use \OCA\RDS\Service\UserserviceportService;

use Exception;

/**
- Define a new page controller
 */

class PageController extends Controller
{
    private $userserviceMapper;
    private $userId;

    public function __construct($AppName, IRequest $request,  UserserviceportService $userservice, $userId)
    {
        parent::__construct($AppName, $request);
        $this->userId = $userId;
        $this->userservice = $userservice;
    }

    /**
     * @NoCSRFRequired
     * @NoAdminRequired
     */

    public function index()
    {
        return $this->checkUserForRDSActivated('main.research');
    }

    /**
     * @NoCSRFRequired
     * @NoAdminRequired
     */

    public function researchEdit($id)
    {
        return $this->checkUserForRDSActivated('main.research', ['id' => $id]);
    }

    /**
     * Returns a list with all services from rds, which registered for user.
     *
     * @return string a list of strings, which are servicenames
     *
     * @NoAdminRequired
     */

    private function checkUserForRDSActivated($templateIfActivated, $params = [])
    {
        try {
            $service = $this->userservice->find('Owncloud', $this->userId);
            $service = $this->userservice->find('Zenodo', $this->userId);
            return new TemplateResponse('rds', $templateIfActivated, $params);
        } catch (Exception $e) {
            return new TemplateResponse('rds', 'not_authorized');
        }
    }
}

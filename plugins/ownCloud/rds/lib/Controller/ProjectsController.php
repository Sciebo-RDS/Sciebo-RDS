<?php

namespace OCA\RDS\Controller;

use OCP\IRequest;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http;
use \OCA\RDS\Service\ProjectsService;
use OCP\AppFramework\Http\RedirectResponse;

class ProjectsController extends Controller
{
    private $userId;
    private $service;

    use Errors;

    public function __construct($AppName, IRequest $request, ProjectsService $service, $userId)
    {
        parent::__construct($AppName, $request);
        $this->userId = $userId;
        $this->service = $service;
    }

    /**
     * Returns a list with all project in service for user.
     *
     * @return array a list with object with key 'jwt', see $this->show()
     *
     * @NoAdminRequired
     * @NoCSRFRequired
     */

    public function index($servicename)
    {
        return $this->handleNotFound(function ()  use ($servicename) {
            return $this->service->findAll($this->userId, $servicename);
        });
    }

    /**
     * Returns a single project in service from user.
     *
     * @param string $id
     * @return object an object with jwt encoded object with keys
     * 'id', 'authorize_url', 'date'
     *
     * @NoAdminRequired
     * @NoCSRFRequired
     */

    public function show($servicename, $id)
    {
        return $this->handleNotFound(function () use ($servicename, $id) {
            return $this->service->find($this->userId, $servicename, $id);
        });
    }

    /**
     * Add a single project in service from user.
     *
     * @param string $id
     * @return object an object with jwt encoded object with keys
     * 'id', 'authorize_url', 'date'
     *
     * @NoAdminRequired
     */

    public function create($servicename)
    {
        return $this->handleNotFound(function () use ($servicename) {
            return $this->service->insert($this->userId, $servicename);
        });
    }

    /**
     * Removes a single project in service from the user.
     *
     * @param string $id
     * @return bool returns true for success, else false
     *
     * @NoAdminRequired
     */

    public function destroy($servicename, $id)
    {
        return $this->handleNotFound(function () use ($servicename, $id) {
            return $this->service->destroy($this->userId, $servicename, $id);
        });
    }
}

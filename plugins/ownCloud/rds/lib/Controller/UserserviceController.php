<?php

namespace OCA\RDS\Controller;

use OCP\IRequest;
use OCP\AppFramework\Controller;
use OCP\IURLGenerator;
use \OCA\RDS\Service\UserserviceportService;
use \OCA\RDS\Service\RDSService;
use OCP\AppFramework\Http\RedirectResponse;
use \OCA\OAuth2\Db\ClientMapper;
use \OCP\ILogger;


use OCP\AppFramework\Http\TemplateResponse;

class UserserviceController extends Controller
{
    private $userId;
    private $service;
    /** @var ClientMapper */
    private $clientMapper;
    private $urlGenerator;
    private $rdsService;
    private $logger;

    use Errors;

    public function __construct(
        $AppName,
        IRequest $request,
        UserserviceportService $service,
        ClientMapper $clientMapper,
        IURLGenerator $urlGenerator,
        $userId,
        RDSService $rdsService,
        ILogger $logger
    ) {
        parent::__construct($AppName, $request);
        $this->clientMapper = $clientMapper;
        $this->userId = $userId;
        $this->service = $service;
        $this->urlGenerator = $urlGenerator;
        $this->rdsService = $rdsService;
        $this->logger = $logger;
    }

    /**
     * Returns a list with all services from RDS for user.
     *
     * @return array a list with object with key 'jwt', see $this->show()
     *
     * @NoAdminRequired
     * @NoCSRFRequired
     */

    public function index()
    {
        return $this->handleNotFound(function () {
            return $this->service->findAll($this->userId);
        });
    }

    /**
     * Returns a single service from user in RDS.
     *
     * @param string $id
     * @return object an object with jwt encoded object with keys
     * 'id', 'authorize_url', 'date'
     *
     * @NoAdminRequired
     * @NoCSRFRequired
     */

    public function show($id)
    {
        return $this->handleNotFound(function () use ($id) {
            return $this->service->find($id, $this->userId);
        });
    }

    /**
     * Removes a single service from the user in RDS.
     *
     * @param string $id
     * @return bool returns true for success, else false
     *
     * @NoAdminRequired
     */

    public function destroy($id)
    {
        return $this->handleNotFound(function () use ($id) {
            return $this->service->delete($id, $this->userId);
        });
    }

    /**
     * Register a new service for the user in RDS.
     *
     * @param string $id
     * @return bool returns true for success, else false
     *
     * @NoAdminRequired
     * @NoCSRFRequired
     */

    public function register($code, $state)
    {
        $params = [];
        $settings = 0;
        try {
            $this->log("used oauthname: " . $this->rdsService->getOauthValue());
            $client = $this->clientMapper->findByName($this->rdsService->getOauthValue());
            $secret = $client->getSecret();
            $this->log("secret: " . $secret);
            $state = str_replace("FROMSETTINGS", "", $state, $settings);
            $this->log("state: " . $state);

            $result = $this->service->register("Owncloud", $code, $state, $this->userId, $secret);
            if (!$result) {
                $params["error"] = "register was not successful";
            }
        } catch (Exception $e) {
            $params["error"] = $e;
        }

        if ($settings > 0) {
            return new RedirectResponse($this->urlGenerator->linkToRoute('settings.SettingsPage.getPersonal', ["sectionid" => "rds"]));
        }
        return new TemplateResponse('rds', "not_authorized", $params);
    }

    public function log($message)
    {
        $this->logger->debug($message, ['app' => $this->appName]);
    }
}

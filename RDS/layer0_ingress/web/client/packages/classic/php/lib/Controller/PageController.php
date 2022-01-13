<?php

namespace OCA\RDS\Controller;

use \OCA\OAuth2\Db\ClientMapper;
use OCP\IUserSession;
use OCP\IURLGenerator;
use \OCA\RDS\Service\RDSService;

use OCP\IRequest;
use OCP\AppFramework\{
    Controller,
    Http\TemplateResponse
};
use OCP\IConfig;

/**
- Define a new page controller
 */

class PageController extends Controller
{
    protected $appName;
    private $userId;

    /**
     * @var IURLGenerator
     */
    private $urlGenerator;

    /**
     * @var UrlService
     */
    private $urlService;

    private $rdsService;

    private $public_key;
    private $private_key;
    private $jwsBuilder;

    private $config;

    use Errors;


    public function __construct(
        $AppName,
        IRequest $request,
        $userId,
        ClientMapper $clientMapper,
        IUserSession $userSession,
        IURLGenerator $urlGenerator,
        RDSService $rdsService
    ) {
        parent::__construct($AppName, $request);
        $this->appName = $AppName;
        $this->userId = $userId;
        $this->clientMapper = $clientMapper;
        $this->userSession = $userSession;
        $this->urlGenerator = $urlGenerator;
        $this->rdsService = $rdsService;
        $this->urlService = $rdsService->getUrlService();
    }

    /**
     * @NoCSRFRequired
     * @NoAdminRequired
     */
    public function index()
    {
        $policy = new \OCP\AppFramework\Http\EmptyContentSecurityPolicy();
        $url = parse_url(\OC::$server->getConfig()->getAppValue("rds", "cloudURL"));
        $http = $url["scheme"] . "://" . $url["host"] . ":" . $url["port"];
        $ws  = str_replace($url["scheme"], "http", "ws") . "://" . $url["host"] . ":" . $url["port"];
        $policy->addAllowedConnectDomain($http);
        $policy->addAllowedConnectDomain($ws);
        $policy->addAllowedConnectDomain($http);
        $policy->addAllowedConnectDomain($ws);
        $policy->addAllowedScriptDomain($http);
        $policy->addAllowedFrameDomain($http);
        \OC::$server->getContentSecurityPolicyManager()->addDefaultPolicy($policy);

        $userId = $this->userSession->getUser()->getUID();

        $params = [
            'clients' => $this->clientMapper->findByUser($userId),
            'user_id' => $userId,
            'urlGenerator' => $this->urlGenerator,
            "cloudURL" => $this->urlService->getURL(),
            "oauthname" => $this->rdsService->getOauthValue(),
        ];

        return new TemplateResponse('rds', "main.research", $params);
    }
}

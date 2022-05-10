<?php

namespace OCA\RDS\Controller;



use \OCA\OAuth2\Db\ClientMapper;
use OCP\IUserSession;
use OCP\IURLGenerator;
use \OCA\RDS\Service\RDSService;

use OCP\IRequest;
use OCP\AppFramework\ApiController;
use OCP\IConfig;
use OCP\L10N\IFactory;

/**
- Define a new api controller
 */

class RdsApiController extends ApiController
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

    private $config;
    protected $lfactory;

    use Errors;


    public function __construct(
        $AppName,
        IRequest $request,
        $userId,
        ClientMapper $clientMapper,
        IUserSession $userSession,
        IURLGenerator $urlGenerator,
        RDSService $rdsService,
        IConfig $config,
        IFactory $lfactory
    ) {
        parent::__construct($AppName, $request);
        $this->appName = $AppName;
        $this->userId = $userId;
        $this->clientMapper = $clientMapper;
        $this->userSession = $userSession;
        $this->urlGenerator = $urlGenerator;
        $this->rdsService = $rdsService;
        $this->urlService = $rdsService->getUrlService();

        $this->config = $config;
        $this->lfactory = $lfactory;

        $arr = $rdsService->getKeys();
        $this->private_key = $arr[0];
        $this->public_key = $arr[1];
    }

    /**
     * @CORS
     * @NoAdminRequired
     * @NoCSRFRequired
     *
     * Returns the user informations
     *
     * @return object the informations as jwt
     */
    public function informations()
    {
        return $this->handleNotFound(function () {
            $user = \OC::$server->getUserSession()->getUser();
            $data = [
                "email" => $user->getEMailAddress(),
                "name" => $user->getUserName(),
                "displayName" => $user->getDisplayName(),
                "accountId" => $user->getAccountId(),
                "UID" => $user->getUID(),
                "cloudID" => $user->getCloudId(),
                #"lastLogin" => $user->getLastLogin(),
                #"home" => $user->getHome(),
                #"avatarImage" => $user->getAvatarImage($user),
                #"quota" => $user->getQuota(),
                #"searchTerms" => $user->getSearchTerms(),
                #"webdav_type" => "owncloud",
                "serverName" => $_SERVER['SERVER_NAME'],
                "webdav" => $this->rdsService->myServerUrl() . "/remote.php/webdav",
                #"access_token" => "", # maybe for later usage
            ];

            $token = \Firebase\JWT\JWT::encode($data, $this->private_key, 'RS256');
            $activeLangCode = $this->config->getUserValue(
                $this->userSession->getUser()->getUID(),
                'core',
                'lang',
                $this->lfactory->findLanguage()
            );

            return [
                "jwt" => $token,
                "cloudURL" => $this->urlService->getURL(),
                "language" => $activeLangCode,
                "serverName" => $data["serverName"]
            ];
        });
    }

    /**
     * @PublicPage
     * @CORS
     *
     * Returns the public key for mailadress
     *
     * @return object an object with publickey
     */
    public function publickey()
    {
        return $this->handleNotFound(function () {
            $data = [
                "publickey" =>  $this->public_key
            ];
            return $data;
        });
    }
}

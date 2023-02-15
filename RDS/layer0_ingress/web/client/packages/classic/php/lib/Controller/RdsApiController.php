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

use OCP\Share\IManager;
use OCP\Files\Folder;
use OCP\Files\IRootFolder;
use OC\OCS\Result;


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

    /** @var IManager */
    private $shareManager;

    /** @var Folder[] */
    private $currentUserFolder;

    /** @var IRootFolder */
    private $rootFolder;

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
        IFactory $lfactory,
        IRootFolder $rootFolder,

        IManager $shareManager
    ) {
        parent::__construct($AppName, $request);
        $this->appName = $AppName;
        $this->userId = $userId;
        $this->clientMapper = $clientMapper;
        $this->userSession = $userSession;
        $this->urlGenerator = $urlGenerator;
        $this->rdsService = $rdsService;
        $this->urlService = $rdsService->getUrlService();

        $this->rootFolder = $rootFolder;

        $this->config = $config;
        $this->lfactory = $lfactory;

        $this->shareManager = $shareManager;

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
     * Returns root folder of the current user
     * Copied from https://github.com/owncloud/core/blob/b68119d7cdcb97064f479f4aefe31d661eaab792/apps/files_sharing/lib/Controller/Share20OcsController.php#L153
     *
     * @return Folder
     */
    private function getCurrentUserFolder()
    {
        // cache only one key, but be sure to check current user session id in case
        // current user folder changes
        $userSessionId = $this->userSession->getUser()->getUID();
        if (!isset($this->currentUserFolder[$userSessionId])) {
            $this->currentUserFolder = [$userSessionId => $this->rootFolder->getUserFolder($userSessionId)];
        }
        return $this->currentUserFolder[$userSessionId];
    }

    /**
     * @CORS
     * @NoAdminRequired
     * @NoCSRFRequired
     *
     * Heavily inspired by https://github.com/owncloud/core/blob/b68119d7cdcb97064f479f4aefe31d661eaab792/apps/files_sharing/lib/Controller/Share20OcsController.php#L370
     * Returns a public link to given path.
     * In request body it needs a "path" field nothing else.
     *
     * @return object returns needed information to access the share
     */
    public function createShare()
    {
        $date = new \DateTime("now");
        $date->add(\DateInterval::createFromDateString("7 days"));
        $path = $this->request->getParam('path', null);

        if ($path === null) {
            return new Result(null, 404, "missing path");
        }

        try {
            $userFolder = $this->getCurrentUserFolder();
            $path = $userFolder->get($path);
        } catch (\OCP\Files\NotFoundException $e) {
            return new Result(null, 404, "invalid path");
        }

        $share = $this->shareManager->newShare();
        $share->setName("Sciebo RDS temporary share");
        $share->setExpirationDate($date);
        $share->setPermissions(1); # readonly
        $share->setShareType(3); # share as link
        $share->setNode($path);

        $share = $this->shareManager->createShare($share);

        # generate a link to access the share
        $result = ['url' => $this->urlGenerator->linkToRouteAbsolute('files_sharing.sharecontroller.showShare', ['token' => $share->getToken()])];
        return new Result($result);
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

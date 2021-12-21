<?php

namespace OCA\RDS\Controller;

require __DIR__ . '/../../vendor/autoload.php';

use Jose\Component\KeyManagement\JWKFactory;
use Jose\Component\Core\Util\RSAKey;

use \OCA\OAuth2\Db\ClientMapper;
use OCP\IUserSession;
use OCP\IURLGenerator;
use \OCA\RDS\Service\RDSService;

use OCP\IRequest;
use OCP\AppFramework\{
    ApiController,
};
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
    private $jwsBuilder;

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

        $this->jwk = RSAKey::createFromJWK(JWKFactory::createRSAKey(
            4096 // Size in bits of the key. We recommend at least 2048 bits.
        ));

        $this->private_key = $this->config->getAppValue("rds", "privatekey", "");
        $this->public_key = $this->config->getAppValue("rds", "publickey", "");

        if ($this->private_key === "") {
            $this->public_key = RSAKey::toPublic($this->jwk)->toPEM();
            $this->private_key = $this->jwk->toPEM();

            $this->config->setAppValue("rds", "privatekey", $this->private_key);
            $this->config->setAppValue("rds", "publickey", $this->public_key);
        }
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
        function my_server_url()
        {
            $server_name = $_SERVER['SERVER_NAME'];

            if (!in_array($_SERVER['SERVER_PORT'], [80, 443])) {
                $port = ":$_SERVER[SERVER_PORT]";
            } else {
                $port = '';
            }

            if (!empty($_SERVER['HTTPS']) && (strtolower($_SERVER['HTTPS']) == 'on' || $_SERVER['HTTPS'] == '1')) {
                $scheme = 'https';
            } else {
                $scheme = 'http';
            }
            return $scheme . '://' . $server_name . $port;
        }

        return $this->handleNotFound(function () {
            $user = \OC::$server->getUserSession()->getUser();
            $data = [
                "email" => $user->getEMailAddress(),
                "name" => $user->getUserName(),
                "displayName" => $user->getDisplayName(),
                "accountId" => $user->getAccountId(),
                "UID" => $user->getUID(),
                "lastLogin" => $user->getLastLogin(),
                "home" => $user->getHome(),
                "avatarImage" => $user->getAvatarImage($user),
                "quota" => $user->getQuota(),
                "searchTerms" => $user->getSearchTerms(),
                "webdav_type" => "owncloud",
                "webdav" => my_server_url() . "/remote.php/webdav",
                "access_token" => "",
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
                "cloudURL" => \OC::$server->getConfig()->getAppValue("rds", "cloudURL"),
                "language" => $activeLangCode
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

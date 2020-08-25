<?php

namespace OCA\RDS\Panels;

use \OCA\OAuth2\Db\ClientMapper;
use OCP\IURLGenerator;
use OCP\IUserSession;
use OCP\Settings\ISettings;
use OCP\Template;
use \OCA\RDS\Service\UrlService;

class AdminPanel implements ISettings
{

    /**
     * @var \OCA\OAuth2\Db\ClientMapper
     */
    protected $clientMapper;
    /**
     * @var IUserSession
     */
    protected $userSession;

    /**
     * @var IURLGenerator
     */
    protected $urlGenerator;

    /**
     * @var UrlService
     */
    protected $urlService;

    protected $config;
    private $oauthname;
    private $appName;

    public function __construct(
        ClientMapper $clientMapper,
        IUserSession $userSession,
        IURLGenerator $urlGenerator,
        UrlService $urlService,
        IConfig $config,
        $appName
    ) {
        $this->clientMapper = $clientMapper;
        $this->userSession = $userSession;
        $this->urlGenerator = $urlGenerator;
        $this->urlService = $urlService;
        $this->config = $config;
        $this->oauthname="oauthname";
        $this->appName = $appName;
    }

    public function getSectionID()
    {
        return 'rds';
    }

    /**
     * @return Template
     */
    public function getPanel()
    {
        $userId = $this->userSession->getUser()->getUID();
        $t = new Template('rds', 'settings-admin');
        $t->assign('clients', $this->clientMapper->findByUser($userId));
        $t->assign('user_id', $userId);
        $t->assign('urlGenerator', $this->urlGenerator);
        $t->assign("cloudURL", $this->urlService->getURL());
        $t->assign("oauthname", $this->config->getAppValue($this->appName, $this->oauthname));
        return $t;
    }

    public function getPriority()
    {
        return 20;
    }
}

<?php

namespace OCA\RDS\Panels;

use \OCA\OAuth2\Db\ClientMapper;
use OCP\IURLGenerator;
use OCP\IUserSession;
use OCP\Settings\ISettings;
use OCP\Template;
use \OCA\RDS\Service\UrlService;
use \OCA\RDS\Service\RDSService;

class AdminPanel implements ISettings
{
    private $appName;
    /**
     * @var \OCA\OAuth2\Db\ClientMapper
     */
    private $clientMapper;
    /**
     * @var IUserSession
     */
    private $userSession;

    /**
     * @var IURLGenerator
     */
    private $urlGenerator;

    /**
     * @var UrlService
     */
    private $urlService;

    private $rdsService;


    public function __construct(
        ClientMapper $clientMapper,
        IUserSession $userSession,
        RDSService $rdsService
    ) {
        $this->appName = "rds";
        $this->clientMapper = $clientMapper;
        $this->userSession = $userSession;
        $this->urlGenerator = \OC::$server->getURLGenerator();
        $this->rdsService = $rdsService;
        $this->urlService = $rdsService->getUrlService();
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
        $t = new Template($this->appName, 'settings-admin');
        $t->assign('clients', $this->clientMapper->findByUser($userId));
        $t->assign('user_id', $userId);
        $t->assign('urlGenerator', $this->urlGenerator);
        $t->assign("cloudURL", $this->urlService->getURL());
        $t->assign("oauthname", $this->rdsService->getOauthValue());
        return $t;
    }

    public function getPriority()
    {
        return 20;
    }
}

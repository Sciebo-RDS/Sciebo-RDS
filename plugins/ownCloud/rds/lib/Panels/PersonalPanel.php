<?php

namespace OCA\RDS\Panels;

use \OCA\OAuth2\Db\ClientMapper;
use OCP\IURLGenerator;
use OCP\Settings\ISettings;
use OCP\Template;
use \OCA\RDS\Service\RDSService;
use OCP\IUserSession;

class PersonalPanel implements ISettings
{
    protected $clientMapper;
    protected $urlGenerator;
    protected $urlService;
    protected $rdsService;
    protected $userSession;

    public function __construct(
        ClientMapper $clientMapper,
        IURLGenerator $urlGenerator,
        IUserSession $userSession,
        RDSService $rdsService
    ) {
        $this->clientMapper = $clientMapper;
        $this->urlGenerator = $urlGenerator;
        $this->userSession = $userSession;
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
        $t = new Template('rds', 'settings-personal');
        $t->assign('clients', $this->clientMapper->findByUser($userId));
        $t->assign('user_id', $userId);
        $t->assign('urlGenerator', $this->urlGenerator);
        $t->assign('rdsURL', $this->urlService->getPortURL());
        $t->assign('oauthname', $this->rdsService->getOauthValue());
        return $t;
    }

    public function getPriority()
    {
        return 20;
    }
}

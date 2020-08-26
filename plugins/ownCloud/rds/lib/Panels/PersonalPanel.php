<?php

namespace OCA\RDS\Panels;

use \OCA\OAuth2\Db\ClientMapper;
use OCP\IURLGenerator;
use OCP\IUserSession;
use OCP\Settings\ISettings;
use OCP\Template;
use OCA\RDS\Service\RDSService;

class PersonalPanel implements ISettings
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
    protected $urlService;

    public function __construct(
        ClientMapper $clientMapper,
        IUserSession $userSession,
        IURLGenerator $urlGenerator,
        RDSService $rdsService
    ) {
        $this->clientMapper = $clientMapper;
        $this->userSession = $userSession;
        $this->urlGenerator = $urlGenerator;
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
        $t->assign("oauthname", $this->rdsService->getOauthValue());
        return $t;
    }

    public function getPriority()
    {
        return 20;
    }
}

<?php

namespace OCA\RDS\Panels;

use \OCA\OAuth2\Db\ClientMapper;
use OCP\IURLGenerator;
use OCP\IUserSession;
use OCP\Settings\ISettings;
use OCP\Template;

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

    public function __construct(
        ClientMapper $clientMapper,
        IUserSession $userSession,
        IURLGenerator $urlGenerator
    ) {
        $this->clientMapper = $clientMapper;
        $this->userSession = $userSession;
        $this->urlGenerator = $urlGenerator;
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
        return $t;
    }

    public function getPriority()
    {
        return 20;
    }

}

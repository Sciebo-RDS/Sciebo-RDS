<?php

namespace OCA\RDS\Service;

use \OCP\IConfig;
use OCA\RDS\Service\UrlService;


class RDSService
{
    protected $urlService;
    private $oauthname;
    private $appName;
    private $config;

    public function __construct(UrlService $urlService, IConfig $config, $appName)
    {
        $this->urlService = $urlService;
        $this->oauthname = "oauthname";
        $this->appName = $appName;
        $this->config = $config;
    }

    public function getUrlService()
    {
        return $this->urlService;
    }

    public function getOauthAppField()
    {
        return $this->oauthname;
    }

    public function getOauthValue()
    {
        return $this->config->getAppValue($this->appName, $this->oauthname);
    }
}

<?php

namespace OCA\RDS\Service;

use \OCP\IConfig;
use \OCP\IURLGenerator;
use OCA\RDS\Service\UrlService;

require_once __DIR__ . '/../../vendor/autoload.php';

use Jose\Component\KeyManagement\JWKFactory;
use Jose\Component\Core\Util\RSAKey;

class RDSService
{
    protected $urlService;
    private $oauthname;
    private $appName;
    private $config;

    public function __construct($AppName, UrlService $urlService, IConfig $config, IURLGenerator $urlGenerator)
    {
        $this->urlService = $urlService;
        $this->oauthname = "oauthname";
        $this->appName = $AppName;
        $this->config = $config;
        $this->urlGenerator = $urlGenerator;
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

    public function createKeys()
    {
        $jwk = RSAKey::createFromJWK(JWKFactory::createRSAKey(
            4096 // Size in bits of the key. We recommend at least 2048 bits.
        ));

        $public_key = RSAKey::toPublic($jwk)->toPEM();
        $private_key = $jwk->toPEM();

        $this->config->setAppValue($this->appName, "privatekey", $private_key);
        $this->config->setAppValue($this->appName, "publickey", $public_key);

        return [$private_key, $public_key];
    }

    /**
     * Returns the private and public key as an array with private key in first place (index 0) and public in second (index 1).
     * 
     */
    public function getKeys()
    {
        $private_key = $this->config->getAppValue($this->appName, "privatekey");
        $public_key = $this->config->getAppValue($this->appName, "publickey");

        return [$private_key, $public_key];
    }

    public function myServerUrl()
    {
        $url = $this->parse_url($this->config->getAppValue($this->appName, "cloudURL"));
        if (!$url) {
            $url = $this->parse_url($this->urlGenerator->getAbsoluteURL("/"));
        }

        return $url["scheme"] . "://" . $url["host"] . ":" . $url["port"];
    }

    private function parse_url($url)
    {
        $url = parse_url($url);

        if (!isset($url["scheme"]) or empty($url["scheme"]) or !$url["scheme"]) {
            $url["scheme"] = "443";
        }

        if (!isset($url["port"]) or empty($url["port"]) or !$url["port"]) {
            $url["port"] = ($url["scheme"] == "http") ? "80" : "443";
        }

        return $url;
    }

    public function execute_reset()
    {
        $url = $this->parse_url($this->urlGenerator->getAbsoluteURL("/"));
        $url = $url["scheme"] . "://rds." . $url["host"] . ":" . $url["port"];

        $this->config->setAppValue("rds", $this->urlService->getCloudUrlKey(), $url);
        $this->config->setAppValue("rds", $this->getOauthAppField(), "rds");

        $this->createKeys();
    }
}

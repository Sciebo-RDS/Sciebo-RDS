<?php

# $app = new \OCP\AppFramework\App('RDS');


$server = \OC::$server;
$server->getNavigationManager()->add(function () {
    $server = \OC::$server;
    $urlGenerator = $server->getURLGenerator();
    return [
        // The string under which your app will be referenced in owncloud
        'id' => 'rds',

        // The sorting weight for the navigation.
        // The higher the number, the higher will it be listed in the navigation
        'order' => 10,

        // The route that will be shown on startup
        'href' => $urlGenerator->linkToRoute('rds.page.index'),

        // The icon that will be shown in the navigation, located in img/
        'icon' => $urlGenerator->imagePath('rds', 'research-white.svg'),

        // The application's title, used in the navigation & the settings page of your app
        'name' => $server->getL10N('rds')->t('RDS App'),
    ];
});

/*
use OCA\RDS\Service\RDSService;
use \OCP\Util;
use \OCP\AppFramework\Http\EmptyContentSecurityPolicy;

$eventDispatcher = $server->getEventDispatcher();
$eventDispatcher->addListener('OCA\Files::loadAdditionalScripts', function () {
    $server = \OC::$server;
    $policy = new EmptyContentSecurityPolicy();

    $val = $server->query(RDSService::class)->myServerUrl();

    $url = parse_url($val);
    $policy->addAllowedConnectDomain($url["scheme"] . "://" . $url["host"] . ":" . $url["port"]);
    $policy->addAllowedConnectDomain(str_replace($url["scheme"], "http", "ws") . "://" . $url["host"] . ":" . $url["port"]);
    \OC::$server->getContentSecurityPolicyManager()->addDefaultPolicy($policy);


    Util::addScript('rds', "socket.io.min");
    Util::addScript('rds', 'fileActions');
    Util::addStyle("rds", "style");
});
*/
<?php

\OC::$server->getNavigationManager()->add(function () {
    $urlGenerator = \OC::$server->getURLGenerator();
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
        'name' => \OC::$server->getL10N('rds')->t('RDS App'),
    ];
});

use OCP\Util;

$eventDispatcher = \OC::$server->getEventDispatcher();
$eventDispatcher->addListener('OCA\Files::loadAdditionalScripts', function () {
    $policy = new \OCP\AppFramework\Http\EmptyContentSecurityPolicy();
    $url = parse_url(\OC::$server->getConfig()->getAppValue("rds", "cloudURL"));
    $policy->addAllowedConnectDomain($url["scheme"] . "://" . $url["host"] . ":" . $url["port"]);
    $policy->addAllowedConnectDomain(str_replace($url["scheme"], "http", "ws") . "://" . $url["host"] . ":" . $url["port"]);
    \OC::$server->getContentSecurityPolicyManager()->addDefaultPolicy($policy);

    Util::addScript('rds', "socket.io.min");
    Util::addScript('rds', 'fileActions');
    Util::addStyle("rds", "style");
});

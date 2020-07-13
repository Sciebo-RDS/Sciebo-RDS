<?php

namespace OCA\RDS\AppInfo;

use \OCP\AppFramework\App;
use \OCA\RDS\Controller\PageController;

use \OCA\RDS\Db\ServiceMapper;
use \OCA\RDS\Service\ServiceportService;
use \OCA\RDS\Controller\ServiceController;

use \OCA\RDS\Db\UserserviceMapper;
use \OCA\RDS\Service\UserserviceportService;
use \OCA\RDS\Controller\UserserviceController;

use \OCA\RDS\Db\ResearchMapper;
use \OCA\RDS\Service\ResearchService;
use \OCA\RDS\Controller\ResearchController;

use \OCA\RDS\Db\MetadataMapper;
use \OCA\RDS\Service\MetadataService;
use \OCA\RDS\Controller\MetadataController;


use \OCA\RDS\Db\ProjectsMapper;
use \OCA\RDS\Service\ProjectsService;
use \OCA\RDS\Controller\ProjectsController;

use \OCA\RDS\Service\UrlService;


class Application extends App
{
    public function __construct(array $urlParams = array())
    {
        parent::__construct('rds', $urlParams);

        $container = $this->getContainer();

        $container->registerService('Logger', function ($c) {
            return $c->query('ServerContainer')->getLogger();
        });

        $container->registerService("UrlService", function ($c) {
            return new UrlService(
                $c->query('Config'),
                $c->query('AppName')
            );
        });

        $container->registerService("ServiceMapper", function ($c) {
            return new ServiceMapper(
                $c->query('UrlService'),
                $c->query('UserId')
            );
        });
        $container->registerService("ServiceportService", function ($c) {
            return new ServiceportService($c->query("ServiceMapper"));
        });
        $container->registerService('ServiceController', function ($c) {
            return new ServiceController(
                $c->query('AppName'),
                $c->query('Request'),
                $c->query("ServiceportService")
            );
        });

        $container->registerService("UserserviceMapper", function ($c) {
            return new UserserviceMapper($c->query('UrlService'));
        });
        $container->registerService("UserserviceportService", function ($c) {
            return new UserserviceportService($c->query("UserserviceMapper"));
        });
        $container->registerService('UserserviceController', function ($c) {
            return new UserserviceController(
                $c->query('AppName'),
                $c->query('Request'),
                $c->query("UserserviceportService"),
                $c->query('\OCA\OAuth2\Db\ClientMapper'),
                $c->query('URLGenerator'),
                $c->query('UserId')
            );
        });

        $container->registerService('URLGenerator', static function ($c) {
            return $c->query('ServerContainer')->getURLGenerator();
        });

        $container->registerService("ResearchMapper", function ($c) {
            return new ResearchMapper(
                $c->query('UrlService'),
                $c->query('Logger'),
                $c->query('AppName')
            );
        });
        $container->registerService("ResearchService", function ($c) {
            return new ResearchService(
                $c->query('Logger'),
                $c->query('AppName'),
                $c->query("ResearchMapper")
            );
        });
        $container->registerService('ResearchController', function ($c) {
            return new ResearchController(
                $c->query('Logger'),
                $c->query('AppName'),
                $c->query('Request'),
                $c->query("ResearchService"),
                $c->query('UserId')
            );
        });

        $container->registerService("ProjectsMapper", function ($c) {
            return new ProjectsMapper($c->query('UrlService'));
        });
        $container->registerService("ProjectsService", function ($c) {
            return new ProjectsService($c->query("ProjectsMapper"));
        });
        $container->registerService('ProjectsController', function ($c) {
            return new ProjectsController(
                $c->query('AppName'),
                $c->query('Request'),
                $c->query("ProjectsService"),
                $c->query('UserId')
            );
        });

        $container->registerService("MetadataMapper", function ($c) {
            return new MetadataMapper($c->query('UrlService'));
        });
        $container->registerService("MetadataService", function ($c) {
            return new MetadataService($c->query("MetadataMapper"));
        });
        $container->registerService('MetadataController', function ($c) {
            return new MetadataController(
                $c->query('AppName'),
                $c->query('Request'),
                $c->query("MetadataService"),
                $c->query("ResearchService"),
                $c->query('UserId')
            );
        });

        $container->registerService('PageController', function ($c) {
            return new PageController(
                $c->query('AppName'),
                $c->query('Request'),
                $c->query("UserserviceportService"),
                $c->query('UserId')
            );
        });

        $container->registerService('Config', function ($c) {
            return $c->query('ServerContainer')->getConfig();
        });
    }
}

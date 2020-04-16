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




class Application extends App {
    public function __construct(array $urlParams=array()){
        parent::__construct('rds', $urlParams);

        $container = $this->getContainer();
        
        $container->registerService("ServiceMapper", function($c) {
            return new ServiceMapper($c->query('UserId'));
        });
        $container->registerService("ServiceportService", function($c) {
            return new ServiceportService($c->query("ServiceMapper"));
        });
        $container->registerService('ServiceController', function($c) {
            return new ServiceController(
                $c->query('AppName'),
                $c->query('Request'),
                $c->query("ServiceportService")
            );
        });
        
        $container->registerService("UserserviceMapper", function($c) {
            return new UserserviceMapper();
        });
        $container->registerService("UserserviceportService", function($c) {
            return new UserserviceportService($c->query("UserserviceMapper"));
        });
        $container->registerService('UserserviceController', function($c) {
            return new UserserviceController(
                $c->query('AppName'),
                $c->query('Request'),
                $c->query("UserserviceportService"),
                $c->query('UserId')
            );
        });
        
        $container->registerService("ResearchMapper", function($c) {
            return new ResearchMapper();
        });
        $container->registerService("ResearchService", function($c) {
            return new ResearchService($c->query("ResearchMapper"));
        });
        $container->registerService('ResearchController', function($c) {
            return new ServiceController(
                $c->query('AppName'),
                $c->query('Request'),
                $c->query("ResearchService"),
                $c->query('UserId')
            );
        });
        
        $container->registerService("MetadataMapper", function($c) {
            return new MetadataMapper();
        });
        $container->registerService("MetadataService", function($c) {
            return new MetadataService($c->query("MetadataMapper"));
        });
        $container->registerService('MetadataController', function($c) {
            return new ServiceController(
                $c->query('AppName'),
                $c->query('Request'),
                $c->query("MetadataService"),
                $c->query('UserId')
            );
        });

        $container->registerService('PageController', function($c) {
            return new PageController(
                $c->query('AppName'),
                $c->query('Request'),
                $c->query('\OCA\OAuth2\Db\ClientMapper'),
                $c->query("UserserviceportService"),
                $c->query('UserId')
            );
        });
        
    }
}

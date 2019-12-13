<?php
namespace OCA\RDS\AppInfo;

use \OCP\AppFramework\App;
use \OCA\RDS\Controller\PageController;
use \OCA\RDS\Controller\ServiceAPIController;

class Application extends App {
    public function __construct(array $urlParams=array()){
        parent::__construct('rds', $urlParams);

        $container = $this->getContainer();

        $container->registerService('PageController', function($c) {
            return new PageController(
                $c->query('AppName'),
                $c->query('Request'),
                $c->query('OCA\OAuth2\Db\ClientMapper'),
                $c->query('UserId')
            );
        });

        $container->registerService('ServiceAPIController', function($c) {
            return new ServiceAPIController(
                $c->query('AppName'),
                $c->query('Request'),
                $c->query('UserId')
            );
        });
    }
}

<?php
namespace OCA\RDS\AppInfo;

use \OCP\AppFramework\App;
use \OCA\RDS\Controller\PageController;

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
    }
}

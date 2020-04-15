<?php
namespace OCA\RDS\AppInfo;

use OCP\AppFramework\App;
use OCA\RDS\Controller\PageController;

use OCA\RDS\Controller\ServiceController;
use OCA\RDS\Db\ServiceMapper;
use OCA\RDS\Service\ServiceportService;

use OCA\RDS\Controller\ResearchController;
use OCA\RDS\Service\ResearchService;
use OCA\RDS\Db\ResearchMapper;

use OCA\RDS\Controller\MetadataController;
use OCA\RDS\Service\MetadataService;
use OCA\RDS\Db\MetadataMapper;




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

        $servicemapper = new ServiceMapper();
        $serviceportservice = new ServiceportService($servicemapper);

        $container->registerService('ServiceController', function($c) {
            return new ServiceController(
                $c->query('AppName'),
                $c->query('Request'),
                $serviceportservice,
                $c->query('UserId')
            );
        });

        $researchmapper = new ResearchMapper();
        $researchservice = new ResearchService($researchmapper);

        $container->registerService('ResearchController', function($c) {
            return new ResearchController(
                $c->query('AppName'),
                $c->query('Request'),
                $researchservice,
                $c->query('UserId')
            );
        });

        $metadatamapper = new MetadataMapper();
        $metadataservice = new MetadataService($metadatamapper);

        $container->registerService('MetadataController', function($c) {
            return new MetadataController(
                $c->query('AppName'),
                $c->query('Request'),
                $metadataservice,
                $c->query('UserId')
            );
        });
    }
}

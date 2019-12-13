<?php

namespace OCA\RDS\AppInfo;

$application = new Application();
$application->registerRoutes($this, [
    'routes' => [
        ['name' => 'page#index',                            'url' => '/',                                       'verb' => 'GET'],

        # API endpoints
        ['name' => 'service#index',                         'url' => '/api/v1/service',                         'verb' => 'GET'],
        ['name' => 'service#show',                          'url' => '/api/v1/service/{servicename}',           'verb' => 'GET'],
        ['name' => 'service#removeServiceFromUser',         'url' => '/api/v1/service/{servicename}/delete',    'verb' => 'POST'],
        ['name' => 'service#getRegisteredServicesForUser',  'url' => '/api/v1/user/service',                    'verb' => 'GET'],
    ]
]);

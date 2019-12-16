<?php

namespace OCA\RDS\AppInfo;

$application = new Application();
$application->registerRoutes($this, [
    'routes' => [
        ['name' => 'page#index',                            'url' => '/',                                       'verb' => 'GET'],

        # API endpoints
        ['name' => 'service_api#index',                         'url' => '/api/v1/service',                         'verb' => 'GET'],
        ['name' => 'service_api#show',                          'url' => '/api/v1/service/{servicename}',           'verb' => 'GET'],
        ['name' => 'service_api#removeServiceFromUser',         'url' => '/api/v1/service/{servicename}/delete',    'verb' => 'POST'],
        ['name' => 'service_api#getRegisteredServicesForUser',  'url' => '/api/v1/user/service',                    'verb' => 'GET'],
    ]
]);

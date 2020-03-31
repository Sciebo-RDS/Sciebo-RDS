<?php

namespace OCA\RDS\AppInfo;

$application = new Application();
$application->registerRoutes( $this, [
    'resources' => [
        # Connection intern API Endpoints
        'research' => ['url' => '/research'],

        # Service intern API Endpoints
        'service' => ['url' => '/service'],
    ],
    'routes' => [
        ['name' => 'page#index',                                'url' => '/research',                             'verb' => 'GET'],
        ['name' => 'page#connectionShow',                       'url' => '/research/{id}',                        'verb' => 'GET'],
        ['name' => 'page#connectionEdit',                       'url' => '/research/{id}/edit',                   'verb' => 'GET'],

        # Service API endpoints
        ['name' => 'service_api#getRegisteredServicesForUser',  'url' => '/user/service',                           'verb' => 'GET'],
    ]
] );

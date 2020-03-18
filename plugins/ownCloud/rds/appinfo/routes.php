<?php

namespace OCA\RDS\AppInfo;

$application = new Application();
$application->registerRoutes( $this, [
    'resources' => [
        # Connection intern API Endpoints
        'connection' => ['url' => '/connection'],

        # Service intern API Endpoints
        'service' => ['url' => '/service'],
    ],
    'routes' => [
        ['name' => 'page#index',                                'url' => '/connection',                             'verb' => 'GET'],
        ['name' => 'page#connectionShow',                       'url' => '/connection/{id}',                        'verb' => 'GET'],
        ['name' => 'page#connectionEdit',                       'url' => '/connection/{id}/edit',                   'verb' => 'GET'],

        # Service API endpoints
        ['name' => 'service_api#getRegisteredServicesForUser',  'url' => '/user/service',                           'verb' => 'GET'],
    ]
] );

<?php

namespace OCA\RDS\AppInfo;

$application = new Application();
$application->registerRoutes( $this, [
    'resources' => [
        # Research resource API Endpoints, full CRUD
        'research' => ['url' => '/research'],

        # Service resource API Endpoints, full CRUD
        'service' => ['url' => '/service'],

        # Metadata resource API Endpoints, only index/show/update
        'metadata' => ['url' => '/metadata'],
    ],
    'routes' => [
        # template endpoints
        ['name' => 'page#index',                              'url' => '/research',                             'verb' => 'GET'],
        ['name' => 'page#researchShow',                       'url' => '/research/{id}',                        'verb' => 'GET'],
        ['name' => 'page#researchEdit',                       'url' => '/research/{id}/edit',                   'verb' => 'GET'],

        # Service additional API endpoint
        ['name' => 'service#getRegisteredServicesForUser',    'url' => '/service/user',                         'verb' => 'GET'],

        # Metadata additional API endpoint
        ['name' => 'metadata#jsonschema',                     'url' => '/metadata/jsonschema',                  'verb' => 'GET'],
    ]
] );

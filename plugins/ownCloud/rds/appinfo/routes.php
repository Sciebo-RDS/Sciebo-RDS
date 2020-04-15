<?php

namespace OCA\RDS\AppInfo;

$application = new Application();
$application->registerRoutes( $this, [
    'resources' => [
        # Research resource API Endpoints, full CRUD
        'research' => ['url' => '/research'],

        # Service resource API Endpoints, only index/show
        'service' => ['url' => '/service'],

        # User Service resource API Endpoints, only index/show/delete
        'userservice' => ['url' => '/userservice'],

        # Metadata resource API Endpoints, only index/show/update
        'metadata' => ['url' => '/metadata'],
    ],
    'routes' => [
        # template endpoints
        ['name' => 'page#index',                              'url' => '/research',                             'verb' => 'GET'],
        ['name' => 'page#researchShow',                       'url' => '/research/{id}',                        'verb' => 'GET'],
        ['name' => 'page#researchEdit',                       'url' => '/research/{id}/edit',                   'verb' => 'GET'],

        # Metadata additional API endpoint
        ['name' => 'metadata#jsonschema',                     'url' => '/metadata/jsonschema',                  'verb' => 'GET'],
    ]
] );

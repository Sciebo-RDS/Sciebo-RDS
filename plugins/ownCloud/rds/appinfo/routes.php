<?php
return [
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
        ['name' => 'page#index',                              'url' => '/',                                'verb' => 'GET'],
        ['name' => 'page#researchEdit',                       'url' => '/edit/{id}',                       'verb' => 'GET'],

        # Metadata additional API endpoint
        ['name' => 'metadata#jsonschema',                     'url' => '/metadata/jsonschema',             'verb' => 'GET'],

        # Research additional API endpoint
        ['name' => 'research#filesIndex',                     'url' => '/research/files',                  'verb' => 'GET'],
        ['name' => 'research#filesIndexUpload',               'url' => '/research/files',                  'verb' => 'POST'],
        ['name' => 'research#deleteUser',                     'url' => '/research',                        'verb' => 'DELETE'],
        ['name' => 'research#filesGet',                       'url' => '/research/{id}/files',             'verb' => 'GET'],
        ['name' => 'research#filesTrigger',                   'url' => '/research/{id}/files',             'verb' => 'POST'],
        ['name' => 'research#filesSettingsGet',               'url' => '/research/{id}/settings',          'verb' => 'GET'],
        ['name' => 'research#filesSettingsUpdate',            'url' => '/research/{id}/settings',          'verb' => 'PUT'],
        ['name' => 'research#publish',                        'url' => '/research/{id}/publish',           'verb' => 'POST'],

        # User Service resource API Endpoints, index/show/create/delete
        ['name' => 'projects#index',            'url' => '/userservice/{servicename}/projects',             'verb' => 'GET'],
        ['name' => 'projects#show',             'url' => '/userservice/{servicename}/projects/{id}',        'verb' => 'GET'],
        ['name' => 'projects#create',           'url' => '/userservice/{servicename}/projects',             'verb' => 'POST'],
        ['name' => 'projects#destroy',          'url' => '/userservice/{servicename}/projects/{id}',        'verb' => 'DELETE'],

        ['name' => 'Userservice#register',      'url' => '/oauth',                                          'verb' => 'GET']

    ]
];

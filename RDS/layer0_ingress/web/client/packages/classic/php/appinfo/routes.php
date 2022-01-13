<?php
return [
    'routes' => [
        # template endpoints
        ['name' => 'page#index',                'url' => '/',                       'verb' => 'GET'],
        ['name' => 'rds_api#informations',      'url' => '/api/1.0/informations',   'verb' => 'GET'],
        ['name' => 'rds_api#publickey',         'url' => '/api/1.0/publickey',      'verb' => 'GET'],
        [
            'name' => 'rds_api#preflighted_cors',
            'url' => '/api/1.0/{path}',
            'verb' => 'OPTIONS',
            'requirements' => array('path' => '.+')
        ],
    ]
];

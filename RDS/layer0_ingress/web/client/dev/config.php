<?php
$CONFIG = array (
  'apps_paths' => 
  array (
    0 => 
    array (
      'path' => '/var/www/owncloud/apps',
      'url' => '/apps',
      'writable' => false,
    ),
    1 => 
    array (
      'path' => '/var/www/owncloud/custom',
      'url' => '/custom',
      'writable' => true,
    ),
  ),
  'trusted_domains' => 
  array (
    0 => 'localhost',
  ),
  'datadirectory' => '/mnt/data/files',
  'dbtype' => 'mysql',
  'dbhost' => 'mariadb:3306',
  'dbname' => 'owncloud',
  'dbuser' => 'owncloud',
  'dbpassword' => 'owncloud',
  'dbtableprefix' => 'oc_',
  'log_type' => 'owncloud',
  'supportedDatabases' => 
  array (
    0 => 'sqlite',
    1 => 'mysql',
    2 => 'pgsql',
  ),
  'upgrade.disable-web' => true,
  'default_language' => 'en',
  'overwrite.cli.url' => 'http://localhost:8000/',
  'htaccess.RewriteBase' => '/',
  'logfile' => '/mnt/data/files/owncloud.log',
  'loglevel' => 2,
  'memcache.local' => '\\OC\\Memcache\\APCu',
  'mysql.utf8mb4' => true,
  'filelocking.enabled' => true,
  'memcache.distributed' => '\\OC\\Memcache\\Redis',
  'memcache.locking' => '\\OC\\Memcache\\Redis',
  'redis' => 
  array (
    'host' => 'redis',
    'port' => '6379',
  ),
  'passwordsalt' => 'yJDnfNHYXvlSzippDha8Lyi4WVYny9',
  'secret' => 'AFLFJDVq9fCtLvItUNaJvlk+vAQgbIShNXa4ne9NHCnj9jDf',
  'version' => '10.7.0.4',
  'logtimezone' => 'UTC',
  'installed' => true,
  'instanceid' => 'ocq54to2dkpc',
  'web.baseUrl' => 'http://localhost:9100',
  'cors.allowed-domains' => ['http://localhost:9100'],
);
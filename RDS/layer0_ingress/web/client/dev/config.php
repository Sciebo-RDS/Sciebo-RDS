<?php
$CONFIG = array (
  'debug' => true,
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
  'log_type' => 'syslog',
  'supportedDatabases' => 
  array (
    0 => 'sqlite',
    1 => 'mysql',
    2 => 'pgsql',
  ),
  'upgrade.disable-web' => true,
  'default_language' => 'en',
  'overwrite.cli.url' => 'http://localhost/',
  'htaccess.RewriteBase' => '/',
  'logfile' => '/mnt/data/files/owncloud.log',
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
  'passwordsalt' => 'Nvb/B2A1OMkEKMtyMjmVUfcaLbqSro',
  'secret' => 'npBF4n+Tm4+r7m6bgRwXqUvIBF0GBlKp7RfayLXacRSXgijg',
  'version' => '10.7.0.4',
  'logtimezone' => 'UTC',
  'installed' => true,
  'instanceid' => 'ocirjd76unba',
  'loglevel' => 0,
  
  'maintenance' => false,
);

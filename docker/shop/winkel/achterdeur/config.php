<?php

$selfAddress = getenv('SELF_ADDRESS');

// HTTP
define('HTTP_SERVER', $selfAddress . '/winkel/achterdeur/');
define('HTTP_CATALOG', $selfAddress . '/winkel/');

// HTTPS
define('HTTPS_SERVER', $selfAddress . '/winkel/achterdeur/');
define('HTTPS_CATALOG', $selfAddress . '/winkel/');

// DIR
define('DIR_APPLICATION', '//var/www/html/winkel/achterdeur/');
define('DIR_SYSTEM', '//var/www/html/winkel/system/');
define('DIR_DATABASE', '//var/www/html/winkel/system/database/');
define('DIR_LANGUAGE', '//var/www/html/winkel/achterdeur/language/');
define('DIR_TEMPLATE', '//var/www/html/winkel/achterdeur/view/template/');
define('DIR_CONFIG', '//var/www/html/winkel/system/config/');
define('DIR_IMAGE', '//var/www/html/winkel/image/');
define('DIR_CACHE', '//var/www/html/winkel/system/cache/');
define('DIR_DOWNLOAD', '//var/www/html/winkel/download/');
define('DIR_LOGS', '//var/www/html/winkel/system/logs/');
define('DIR_CATALOG', '//var/www/html/winkel/catalog/');

// DB
define('DB_DRIVER', 'mysql');
define('DB_HOSTNAME', getenv('DB_HOSTNAME'));
define('DB_USERNAME', getenv('DB_USERNAME'));
define('DB_PASSWORD', getenv('DB_PASSWORD'));
define('DB_DATABASE', getenv('DB_NAME'));
define('DB_PREFIX', getenv('DB_PREFIX'));
?>

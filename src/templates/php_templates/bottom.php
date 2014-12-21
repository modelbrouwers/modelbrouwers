<?php
    // FIXME: unify
    $root = dirname(__FILE__).'/';
    include($root.'settings.php');
    require_once($root.'../../phpbb/php-static-files/static.php');

    $cache = new StaticCache();
	$cache->init();
	$storage = new CachedFilesStorage($cache);
?>

<div id="shop-footer">
    <?php include($root.'footer_banner.php'); ?>
</div>

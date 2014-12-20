<?php
    //echo 'foo';
    $root = dirname(__FILE__).'/';
    //echo $root;
    include($root.'settings.php');
    require_once($root.'../../../php-static-files/static.php');

    $cache = new StaticCache();
	$cache->init();
	$storage = new CachedFilesStorage($cache);

    // TODO: look into Twig templating so we can reuse django templates
?>

<div id="shop-footer">
    <?php include($root.'footer_banner.php'); ?>
</div>

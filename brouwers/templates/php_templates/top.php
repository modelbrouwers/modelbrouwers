<?php
    //echo 'foo';
    $root = dirname(__FILE__).'/';
    //echo $root;
    include($root.'settings.php');

    // TODO: look into H2O templating so we can reuse django templates
?>

<div id="top">
    <div id="navigation">
        <?php include($root.'nav_tabs.php'); ?>
    </div>
    <div id="shop_banner">
        <?php include($root.'shop_banner.php'); ?>
    </div>
    <div id="anniversary"></div>
</div>

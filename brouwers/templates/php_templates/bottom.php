<?php 
    //echo 'foo';
    $root = dirname(__FILE__).'/';
    //echo $root;
    include($root.'settings.php');

    // TODO: look into H2O templating so we can reuse django templates
?>

<div id="shop-footer">
    <?php include($root.'footer_banner.php'); ?>
</div>

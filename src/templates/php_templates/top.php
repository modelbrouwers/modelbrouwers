<?php
    $root = dirname(__FILE__).'/';
    require_once $root.'settings.php';
    // TODO: look into Twig templating so we can reuse django templates
?>

<header class="container-fluid">
    <div class="navbar navbar-default navbar-center sprue-tabs" role="navigation">
        <div class="container-fluid">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="sr-only">Toon/verberg navigatie</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="/">
                    <img src="/static/images/logo/logo_modelbrouwers.png" alt="Terug naar de homepage">
                </a>
            </div>

            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav" id="main-nav">
                    <?php include($root.'nav_tabs.php'); ?>
                </ul>
            </div><!--/.nav-collapse -->
        </div><!--/.container-fluid -->
    </div>

    <ul id="shop-banner">
        <?php include($root.'shop_banner.php'); ?>
    </ul>
</header>

#!/usr/bin/env php
<?php

require __DIR__ . DIRECTORY_SEPARATOR . '..' . DIRECTORY_SEPARATOR . '..' . DIRECTORY_SEPARATOR . 'conf' . DIRECTORY_SEPARATOR . 'settings.php';
require $settings->COMPOSER_AUTOLOADER;

use brouwers\SystemJS\Console\Command\BundleCommand;
use Symfony\Component\Console\Application;

$application = new Application();
$application->add(new BundleCommand());
$application->run();

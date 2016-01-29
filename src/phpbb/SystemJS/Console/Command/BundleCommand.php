<?php

// TODO: maybe we can leverage the PHP tokenizer?

namespace brouwers\SystemJS\Console\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;

class BundleCommand extends Command
{
    protected function configure()
    {
        $this
            ->setName('jspm:bundle')
            ->setDescription('Bundle the JSPM apps used in the forum templates.')
            ->addOption(
               'jspm-executable',
               null,
               InputOption::VALUE_REQUIRED,
               'Specify the jspm executable',
               'jspm'
            )
        ;
    }

    protected function execute(InputInterface $input, OutputInterface $output)
    {
        global $settings;

        // this is the token that will be sought after in the template to find all SystemJS apps
        $TOKEN = '// JSPM:SYSTEMJSAPP';
        $REGEX = "@(['\"])(?P<app>.*)['\"][\s,]*{$TOKEN}@";

        $pathBits = array($settings->PROJECT_DIR, 'phpBB3', 'styles');
        $styles = realpath(implode(DIRECTORY_SEPARATOR, $pathBits));
        $output->writeln('<info>Looking for styles in \'' . $styles . '\'</info>');

        $directory = new \RecursiveDirectoryIterator($styles);
        $iterator = new \RecursiveIteratorIterator($directory);
        $templates = new \RegexIterator($iterator, '/^.+\.html$/i', \RecursiveRegexIterator::GET_MATCH);

        $output->writeln('<info>Parsing templates for bundle markers...</info>');
        $appsFound = array();
        foreach ($templates as $name => $fileObj) {
            $handle = fopen($name, 'r');
            while (($line = fgets($handle)) !== false) {
                if (strpos($line, $TOKEN) !== false) {
                    if (preg_match($REGEX, $line, $m)) {
                        $appsFound[$name][] = $m['app'];
                    }
                }
            }
            fclose($handle);
        }

        $apps = array_reduce($appsFound, function($reduced, $_apps) {
            return array_merge($reduced, $_apps);
        }, array());
        $numApps = count($apps);
        $numTemplates = count(array_keys($appsFound));

        $output->writeln("<info>Found {$numApps} apps in {$numTemplates} templates</info>");

        $jspm = $input->getOption('jspm-executable');
        $cmdTpl = "{$jspm} bundle %s %s 2> /dev/null";
        $systemjsDir = $settings->STATIC_ROOT . DIRECTORY_SEPARATOR . $settings->SYSTEMJS_OUTPUT_DIR;
        if (!is_dir($systemjsDir)) {
            mkdir($systemjsDir);
        }
        $systemjsDir = realpath($systemjsDir);

        foreach ($apps as $app) {
            $file = $systemjsDir . DIRECTORY_SEPARATOR . $app;
            $dest = $file;
            $cmd = sprintf($cmdTpl, $app, $dest);
            $output->writeln("<comment>Bundling \"{$app}\" ...</comment>");
            $output->writeln($cmd);
            $_output = exec($cmd, $out, $exitCode);

            // add the System.import statement
            // TODO: extract the last line (sourcemapping) and paste it at the end
            $js = file_get_contents($dest);
            $js .= "\nSystem.import('{$app}');\n";
            file_put_contents($dest, $js);

            if ($exitCode != 0 || !is_file($dest)) {
                $output->writeln("<error>Bundle for \"$app\" failed...</error>");
            }

            // post process
            $hash = md5_file($dest);
            $hash = substr($hash, 0, 12);

            $info = pathinfo($file);

            $link = $info['dirname'] . DIRECTORY_SEPARATOR . $info['filename'] . '.' . $hash . '.' . $info['extension'];
            if (!is_file($link)) {
                symlink($dest, $link);
                $relative = substr($link, strlen($settings->STATIC_ROOT) + 1);
                $output->writeln("<info>Post-processed file \"{$relative}\"</info>");
            } else {
                $output->writeln("<info>Skipped post-processing: link exists</info>");
            }
        }
    }
}

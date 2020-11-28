<?php

$settingsFile = dirname(dirname(__DIR__)) . DIRECTORY_SEPARATOR . 'conf' . DIRECTORY_SEPARATOR . 'settings.php';
require_once $settingsFile;
require_once __DIR__ . DIRECTORY_SEPARATOR . 'cache.php';
require_once $settings->COMPOSER_AUTOLOADER;
require_once $settings->PROJECT_DIR . DIRECTORY_SEPARATOR . 'errorhandler.php';


class StaticFilesStorage
{

    protected $location = null;
    protected $base_url = null;
    public $DEBUG = false;

    public function __construct() {
        global $settings;
        $this->DEBUG = (bool) getenv('DEBUG');
        $this->location = $settings->STATIC_ROOT;
        $this->base_url = $settings->STATIC_URL;
    }

    /**
     * Get the url to the static file, either from cache or calculate the hashed path.
     */
    public function url($file) {
        return $this->base_url . $file;
    }

    public function get_location() {
        return $this->location;
    }

    public function get_base_url() {
        return $this->base_url;
    }
}


class ManifestStaticFilesStorage extends StaticFilesStorage
{

    protected $manifest_name = 'staticfiles.json';
    protected $hashed_files = null;
    protected $cache = null;

    public function __construct() {
        parent::__construct();
        $this->cache = new StaticCache();
        $this->cache_key_prefix = 'php:staticfiles:';

        // reduce disk IO by caching stuffs
        $key = $this->cache_key_prefix . 'manifest:hashed-files';
        $this->hashed_files = $this->cache->get($key);
        if (!$this->hashed_files) {
            $this->hashed_files = $this->loadManifest();
            $this->cache->set($key, $this->hashed_files, 60 * 60 * 3); // cache for 3 hours
        }
    }

    protected function loadManifest() {
        $content = $this->readManifest();
        if ($content === null) {
            return array();
        }
        $stored = json_decode($content, true);
        $version = $stored['version'];
        if ($version == '1.0') {
            return $stored['paths'] ?: array();
        }
        throw new Exception("Couldn't load manifest - unknown version {$version}");
    }

    protected function readManifest() {
        $path = $this->location . DIRECTORY_SEPARATOR . $this->manifest_name;
        $content = file_get_contents($path);
        return $content;
    }

    public function url($file) {
        if ($this->DEBUG) return $this->base_url . $file;
        return $this->base_url . $this->getStoredName($file);
    }

    protected function getStoredName($file) {
        return $this->hashed_files[$file] ?: null;
    }
}

?>

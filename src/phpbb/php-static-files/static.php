<?php

$settingsFile = dirname(dirname(__DIR__)) . DIRECTORY_SEPARATOR . 'conf' . DIRECTORY_SEPARATOR . 'settings.php';
require_once $settingsFile;
require_once __DIR__ . DIRECTORY_SEPARATOR . 'cache.php';
require_once $settings->COMPOSER_AUTOLOADER;

$DEBUG = false;

// initialize the cache
// $cache = new StaticCache();
// $cache->init();

/**
 * This class builds the hashed filenames similar to Django's cached storage.
 * Because PHP is a lot dumber and I don't want to spend too much effort,
 * we assume Django's collectstatic has been run and the files are present.
 * For when a file is thus requested, we calculate the hash and cache it in
 * Memcached. If the hashed file doesn't exist, return the unchanged URL.
 * Django updates the cached filenames as part of the collectstatic command.
 */
class CachedFilesStorage
{
	private static $static_root;
	private static $static_url;
	private static $cache_key_prefix;

	protected $cache = null;
	protected $DEBUG;

	public function __construct($cache) {
		global $settings;
		$this->static_url = $settings->STATIC_URL;
		$this->cache_key_prefix = 'staticfiles:';
		$this->static_root = $settings->STATIC_ROOT;
		$this->cache = $cache;
		$this->DEBUG = (bool) getenv('DEBUG');
	}

	protected function get_static_root() {
		return $this->static_root;
	}

	protected function get_static_url() {
		return $this->static_url;
	}

	protected function get_hashed_name($file) {
		if($this->DEBUG) return $file;
		$abs_path = realpath($this->static_root . DIRECTORY_SEPARATOR . $file);

		$pathinfo = pathinfo($file);
		$dirname = $pathinfo['dirname'];
		$filename = $pathinfo['filename'];
		$extension = $pathinfo['extension'];

		$md5 = md5_file($abs_path);
		$hash = substr($md5, 0, 12);

		$hashed_filename = $filename . '.' . $hash . '.' . $extension;
		$result = $dirname . DIRECTORY_SEPARATOR. $hashed_filename;
		return $result;
	}

	/**
	 * @param $name is the filename relative to the static root
	 */
	protected function cache_key($name) {
		// don't do utf8 encoding, the hashes differ, even with utf8-strings
		return $this->cache_key_prefix.md5($name);
	}

	/**
	 * Get the url to the static file, either from cache or calculate the hashed path.
	 */
	public function url($file) {
		$cache_key = $this->cache_key($file);
		$hashed_name = ($this->DEBUG) ? false : $this->cache->get($cache_key);

		if($hashed_name === false) {
			$hashed_name = $this->get_hashed_name($file);
			if(!$this->DEBUG) $this->cache->set($cache_key, $hashed_name);
		}
		return $this->static_url . $hashed_name;
	}
}

/**
 * Combines an array of static files into one (minified) file.
 * Similar to the 'compress' tag.
 */
class CombinedStaticFilesStorage extends CachedFilesStorage
{
	protected $CACHE_DIR = 'PHP_CACHE';

	protected function get_cache_dir() {
		$dirname = $this->get_static_root() . DIRECTORY_SEPARATOR . $this->CACHE_DIR;
		if (!is_dir($dirname)) {
			mkdir($dirname);
			chmod($dirname, 0755);
		}
		return $dirname;
	}

	public function url($files, $ext='js') {

		if ($this->DEBUG) {
			$urls = array_map(function($path) {
				return $this->get_static_url() . $path;
			}, $files);
			if ($ext == 'js') {
				$glue = "\"></script>\n<script src=\"";
				return implode($glue, $urls);
			}
		}

		$root = $this->get_static_root();
		$file_paths = array();
		$_output = array();

		// calculate all the file hashes to definitely use the latest file
		foreach ($files as $file) {
			$filename = $root . DIRECTORY_SEPARATOR . $this->get_hashed_name($file);
			$file_paths[] = $filename;
		}
		$md5_result = md5(implode("::", $file_paths));
		$destDir = $this->get_cache_dir();
		$dest_file = $destDir . DIRECTORY_SEPARATOR . $md5_result.'.'.$ext;

		if(!is_file($dest_file)) {
			foreach ($file_paths as $filename) {
				$_output[] = file_get_contents($filename);
			}
			$output = implode("\n;", $_output);
			if ($ext == 'js') {
				$output = \JShrink\Minifier::minify($output);
			}
			file_put_contents($dest_file, $output);
		}

		$url = substr($dest_file, strlen($root)+1);
		return $this->get_static_url().$url;
	}
}

?>

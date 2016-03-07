<?php

$settingsFile = dirname(dirname(__DIR__)) . DIRECTORY_SEPARATOR . 'conf' . DIRECTORY_SEPARATOR . 'settings.php';
require_once $settingsFile;
require_once __DIR__ . DIRECTORY_SEPARATOR . 'cache.php';
require_once $settings->COMPOSER_AUTOLOADER;
require_once $settings->PROJECT_DIR . DIRECTORY_SEPARATOR . 'errorhandler.php';


class StaticFilesStorage
{

	protected $base_location = null;
	protected $location = null;
	protected $base_url = null;
	protected $DEBUG = false;

	protected $systemjs_output_dir;

	public function __construct() {
		global $settings;
		$this->DEBUG = (bool) getenv('DEBUG');
		$this->location = $this->base_location = $settings->STATIC_ROOT;
		$this->base_url = $settings->STATIC_URL;
		$this->systemjs_output_dir = $settings->SYSTEMJS_OUTPUT_DIR;
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

	public function get_systemjs_output_dir() {
		return $this->systemjs_output_dir;
	}

	public function system_import($appOrArray) {

		if (!is_array($appOrArray)) {
			$apps = array($appOrArray);
		} else {
			$apps = $appOrArray;
		}

		if ($this->DEBUG) {
			$imports = array_reduce($apps, function($reduced, $app) {
				$reduced .= "\tSystem.import('{$app}');\n";
				return $reduced;
			}, '');
			return "<script type=\"text/javascript\">\n". $imports . "</script>";
		} else {
			return $this->getBundleScripts($apps);
		}
	}

	protected function getBundleScripts($apps) {
		$imports = '';
		foreach ($apps as $app) {
			$filename = $this->systemjs_output_dir . DIRECTORY_SEPARATOR . $app;
			$url = $this->url($filename);
			$imports .= "\n" . "<script type=\"text/javascript\" src=\"{$url}\"></script>";
		}
		return $imports;
	}
}


/**
 * Utility class to inject in the FileSystemStorage class. This takes care of
 * computing/retrieving hashes to files. It's a workaround for mixins...
 */
class HashUtility
{
	protected $storage = null;

	public function __construct($storage) {
		$this->storage = $storage;
	}

	public function get_hashed_name($file) {
		if($this->storage->DEBUG) return $file;
		$abs_path = realpath($this->storage->get_location() . DIRECTORY_SEPARATOR . $file);

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
}


/**
 * This class builds the hashed filenames similar to Django's cached storage.
 * Because PHP is a lot dumber and I don't want to spend too much effort,
 * we assume Django's collectstatic has been run and the files are present.
 * For when a file is thus requested, we calculate the hash and cache it in
 * Memcached. If the hashed file doesn't exist, return the unchanged URL.
 * Django updates the cached filenames as part of the collectstatic command.
 */
class CachedFilesStorage extends StaticFilesStorage
{
	protected $base_url;
	protected $cache_key_prefix;

	protected $cache = null;

	public function __construct($cache) {
		parent::__construct();
		global $settings;
		$this->cache_key_prefix = 'staticfiles:';
		$this->cache = $cache;
		$this->hash_utility = new HashUtility($this);
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
			$hashed_name = $this->hash_utility->get_hashed_name($file);
			if(!$this->DEBUG) $this->cache->set($cache_key, $hashed_name);
		}
		return $this->base_url . $hashed_name;
	}
}


class Compressor {

	protected $CACHE_DIR = 'PHP_CACHE';

	protected $storage;

	public function __construct($storage) {
		$this->storage = $storage;
	}

	/**
	 *  Used in DEBUG mode: return the files as separete <script> entries, no
	 *  compressing is done.
	 */
	public function uncompressed($files, $ext) {
		$base_url = $this->storage->get_base_url();
		$urls = array_map(function($path) use ($base_url) {
			return $base_url . $path;
		}, $files);

		if ($ext == 'js') {
			$glue = "\"></script>\n<script src=\"";
			return implode($glue, $urls);
		} else {
			return '';
		}
	}

	protected function get_cache_dir() {
		$dirname = $this->storage->get_location() . DIRECTORY_SEPARATOR . $this->CACHE_DIR;
		if (!is_dir($dirname)) {
			mkdir($dirname);
			chmod($dirname, 0755);
		}
		return $dirname;
	}

	public function compress($file_paths, $ext) {
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

		return substr($dest_file, strlen($this->storage->get_location())+1);
	}

	public function getBundleScripts($apps) {
		$filenames = array();
		$combinedUrl = $this->storage->url($apps, $ext='js');
		return "<script type=\"text/javascript\" src=\"{$combinedUrl}\"></script>";
	}
}

/**
 * Combines an array of static files into one (minified) file.
 * Similar to the 'compress' tag.
 */
class CombinedCachedStaticFilesStorage extends CachedFilesStorage
{
	public function __construct($cache) {
		parent::__construct($cache);
		$this->compressor = new Compressor($this);
	}

	public function url($files, $ext='js') {
		if ($this->DEBUG) {
			return $this->compressor->uncompressed($files, $ext);
		}

		$file_paths = array();
		$_output = array();

		// calculate all the file hashes to definitely use the latest file
		foreach ($files as $file) {
			$filename = $this->location . DIRECTORY_SEPARATOR . $this->hash_utility->get_hashed_name($file);
			$file_paths[] = $filename;
		}

		$url = $this->compressor->compress($file_paths, $ext);
		return $this->base_url . $url;
	}

	protected function getBundleScripts($apps) {
		return $this->compressor->getBundleScripts($apps);
	}
}


class ManifestStaticFilesStorage extends StaticFilesStorage
{

	protected $manifest_name = 'staticfiles.json';
	protected $hashed_files = null;

	public function __construct() {
		parent::__construct();
		$this->cache = new StaticCache();
		$this->cache_key_prefix = 'php:staticfiles:';

		// reduce disk IO by caching stuffs
		$key = $this->cache_key_prefix . 'manifest:hashed-files';
		$this->hashed_files = $this->cache->get($key);
		if (!$this->hashed_files) {
			$this->hashed_files = $this->loadManifest();
			$this->cache->set($key, $this->hashed_files, 60*60*3); // cache for 3 hours
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


class CombinedManifestStaticFilesStorage extends ManifestStaticFilesStorage
{
	protected $cache_key_prefix;

	public function __construct() {
		parent::__construct();
		$this->hash_utility = new HashUtility($this);
		$this->compressor = new Compressor($this);
		$this->cache = new StaticCache();
		$this->cache_key_prefix = 'php:staticfiles:';
	}

	public function url($files, $ext='js') {
		if ($this->DEBUG) {
			return $this->compressor->uncompressed($files, $ext);
		}

		$file_paths = array();
		$_output = array();

		// calculate all the file hashes to definitely use the latest file
		foreach ($files as $file) {
			$hashed = $this->getStoredName($file) ?: $file;
			$filename = $this->location . DIRECTORY_SEPARATOR . $hashed;
			$file_paths[] = $filename;
		}

		$url = $this->compressor->compress($file_paths, $ext);
		return $this->base_url . $url;
	}

	protected function getBundleScripts($apps) {

		$key = $this->cache_key_prefix . md5(serialize($apps));
		$result = $this->cache->get($key);

		if ($result === false) {
			foreach ($apps as &$app) {
				// $this->getStoredName yields the hash as generated by collectstatic
				// this is different from the bundled hash
				$app = $this->systemjs_output_dir . DIRECTORY_SEPARATOR . $app;
				$app = $this->hash_utility->get_hashed_name($app);
			}
			unset($app);
			$result = $this->compressor->getBundleScripts($apps);
			$this->cache->set($key, $result, 60*60*3); // cache for 3 hours
		}

		return $result;
	}
}

?>

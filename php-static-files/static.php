<?php

require_once 'cache.php';
$DEBUG = true;

// initialize the cache
$cache = new Cache();
$cache->init();

/**
 * This class builds the hashed filenames similar to Django's cached storage.
 * Because PHP is a lot dumber and I don't want to spend too much effort,
 * we assume Django's collectstatic has been run and the files are present.
 * For when a file is thus requested, we calculate the hash and cache it in
 * Memcached. If the hashed file doesn't exist, return the unchanged URL.
 * Django updates the cached filenames as part of the collectstatic command.
 */
class CachedFilesStorage {

	private static $static_root;
	private static $static_url;
	private static $cache_key_prefix;

	protected $cache = null;
	protected $DEBUG;

	function __construct($cache, $DEBUG=false) {
		$this->static_url = '/static/';
		$this->cache_key_prefix = 'staticfiles:';
		$this->static_root = realpath(dirname(dirname(__FILE__)) . $this->static_url);
		$this->cache = $cache;
		$this->DEBUG = $DEBUG;
	}

	function get_hashed_name($file) {
		if($this->DEBUG) return $file;
		$abs_path = realpath($this->static_root . '/' . $file);

		$pathinfo = pathinfo($file);
		$dirname = $pathinfo['dirname'];
		$filename = $pathinfo['filename'];
		$extension = $pathinfo['extension'];

		$md5 = md5_file($abs_path);
		$hash = substr($md5, 0, 12);

		$hashed_filename = $filename . '.' . $hash . '.' . $extension;
		$result = $dirname . '/'. $hashed_filename;
		return $result;
	}

	/**
	 * @param $name is the filename relative to the static root
	 */
	function cache_key($name) {
		// don't do utf8 encoding, the hashes differ, even with utf8-strings
		return $this->cache_key_prefix.md5($name);
	}

	/**
	 * Get the url to the static file, either from cache or calculate the hashed path.
	 */
	function url($file) {
		$cache_key = $this->cache_key($file);
		$hashed_name = ($this->DEBUG) ? false : $this->cache->get($cache_key);

		if($hashed_name === false) {
			$hashed_name = $this->get_hashed_name($file);
			if(!$this->DEBUG) $this->cache->set($cache_key, $hashed_name);
		}

		return $this->static_url . $hashed_name;
	}
}


$storage = new CachedFilesStorage($cache, $DEBUG);
echo $storage->url('css/albums.css').PHP_EOL;


?>

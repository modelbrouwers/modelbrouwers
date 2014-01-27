<?php
/**
 * This class builds the hashed filenames similar to Django's cached storage.
 * Because PHP is a lot dumber and I don't want to spend too much effor,
 * we assume Django's collectstatic has been run and the files are present.
 * For when a file is thus requested, we calculate the hash and cache it in
 * Memcached. If the hashed file doesn't exist, return the unchanged URL.
 */
class CachedFilesStorage {

	private static $static_root;
	private static $static_url;
	/**
	 * Structure: key: raw filename (relative to the static root), value filename with md5 hash
	 */
	public $m_processed_files;

	function __construct() {
		$this->static_url = '/static/';
		$this->static_root = realpath(dirname(dirname(__FILE__)) . $this->static_url);
	}

	function get_hashed_name($file) {
		$abs_path = realpath($this->static_root . '/' . $file);

		$pathinfo = pathinfo($file);
		$dirname = $pathinfo['dirname'];
		$filename = $pathinfo['filename'];
		$extension = $pathinfo['extension'];

		$md5 = md5_file($abs_path);
		$hash = substr($md5, 0, 12);

		$hashed_filename = $filename . '.' . $hash . '.' . $extension;
		$result = $this->static_url . $dirname . '/'. $hashed_filename;

		$this->m_processed_files[$file] = $result;

		return $result;
	}
}


$storage = new CachedFilesStorage();
echo $storage->get_hashed_name('css/common.css').PHP_EOL;

print_r($storage->m_processed_files);


?>
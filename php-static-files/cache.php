<?php

class StaticCache extends Memcached {
	protected $TIMEOUT = 900; // 15 minutes

	/**
	 * Set up the connection
	 */
	function init() {
		$server_list = $this->getServerList();
		if(count($server_list) === 0) {
			$this->addServer('localhost', 11211);
		}
	}

	function set($key, $value, $expiration=null) {
		if(!$expiration) {
			$expiration = $this->TIMEOUT;
		}
		parent::set($key, $value, $expiration);
	}

}
?>
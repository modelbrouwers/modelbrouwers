(function(win, $, Q) {
	var apiBase = '/api/v1/{0}';

	function ApiRequest(endpoint, data, callback, callbackFailure) {
		this.endpoint = apiBase.format(endpoint);
		this.data = data || {};
		this.callbackSuccess = callback;
		this.callbackFailure = callbackFailure;
	}

	/**
	 * Sends the API call, and executes the callback when completed.
	 * The callback receives the jQuery $.ajax success arguments: data, textStatus, jqXHR
	 */
	ApiRequest.prototype.send = function(method) {
		method = method || 'POST';
		var data = this.data;

		if(!(method == 'GET' || method == 'HEAD')) {
			data = JSON.stringify(this.data);
		}

		var promise = Q($.ajax({
			url: this.endpoint,
			contentType: "application/json",
			type: method,
			data: data
		}));
		promise.then(this.callbackSucces, this.callbackFailure); // different branch
		return promise;
	};

	/**
	 * Wrappers
	 */
	ApiRequest.prototype.get = function() {
		return this.send('GET');
	};

	ApiRequest.prototype.post = function() {
		return this.send('POST');
	};

	ApiRequest.prototype.put = function() {
		return this.send('PUT');
	};


	/**
	 * Constructor
	 */
	function apiRequest(url, data, callback, callbackFailure) {
		return new ApiRequest(url, data || {}, callback, callbackFailure);
	}

	win.Api = {
		request: apiRequest
	};

}(window, jQuery, Q));


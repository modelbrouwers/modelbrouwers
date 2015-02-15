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


/**
* Serializes containers. Example $(".container").serializeObjectV3(); Works also with nested fields
* => <input type="text" name="myName[1][nested]"/> output: myName: { 1 : {nested: value}}
*/
(function () {

	var root = this,
		$ = root.jQuery || root.Zepto || root.ender,
		inputTypes = 'color,date,datetime,datetime-local,email,hidden,month,number,password,range,search,tel,text,time,url,week'.split(','),
		inputNodes = 'select,textarea'.split(','),
		rName = /\[([^\]]*)\]/g;

	// ugly hack for IE7-8
	function isInArray(array, needle) {
		return $.inArray(needle, array) !== -1;
	}

	function storeValue(container, parsedName, value) {

		var part = parsedName[0];

		if (parsedName.length > 1) {
			if (!container[part]) {
				// If the next part is eq to '' it means we are processing complex name (i.e. `some[]`)
				// for this case we need to use Array instead of an Object for the index increment purpose
				container[part] = parsedName[1] ? {} : [];
			}
			storeValue(container[part], parsedName.slice(1), value);
		} else {

			// Increment Array index for `some[]` case
			if (!part) {
				part = container.length;
			}

			container[part] = value;
		}
	}

	$.fn.serializeObject = function (options) {
		options || (options = {});

		var values = {},
			settings = $.extend(true, {
				include: [],
				exclude: [],
				includeByClass: ''
			}, options);

		this.find(':input').each(function () {

			var parsedName;

			// Apply simple checks and filters
			if (!this.name || this.disabled ||
				isInArray(settings.exclude, this.name) ||
				(settings.include.length && !isInArray(settings.include, this.name)) ||
				this.className.indexOf(settings.includeByClass) === -1) {
				return;
			}

			// Parse complex names
			// JS RegExp doesn't support "positive look behind" :( that's why so weird parsing is used
			parsedName = this.name.replace(rName, '[$1').split('[');
			if (!parsedName[0]) {
				return;
			}

			if (this.checked ||
				isInArray(inputTypes, this.type) ||
				isInArray(inputNodes, this.nodeName.toLowerCase())) {

				// Simulate control with a complex name (i.e. `some[]`)
				// as it handled in the same way as Checkboxes should
				if (this.type === 'checkbox') {
					parsedName.push('');
				}

				// jQuery.val() is used to simplify of getting values
				// from the custom controls (which follow jQuery .val() API) and Multiple Select
				storeValue(values, parsedName, $(this).val());
			}
		});

		return values;
	};

}).call(this);

// CSRF protection, code from Django docs
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrf_token = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});

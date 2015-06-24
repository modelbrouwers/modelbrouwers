import $ from 'jquery';
import Q from 'q';

import 'scripts/strformat';
import 'scripts/jquery.serializeObject';
import 'scripts/csrf';


var apiBase = '/api/v1/{0}';

class Api {
    constructor(endpoint, data) {
        this.endpoint = apiBase.format(endpoint);
        this.data = data || {};
    }

    send(method) {
        var data,
            promise;
        method = method || 'POST';

        if(!(method == 'GET' || method == 'HEAD')) {
			data = JSON.stringify(this.data);
		}

		promise = Q($.ajax({
			url: this.endpoint,
			contentType: "application/json",
			type: method,
			data: data
		}));
		return promise;
    }

    head() {
        return this.send('HEAD');
    }

    get() {
        return this.send('GET');
    }

    post() {
        return this.send('POST');
    }

    put() {
        return this.send('PUT');
    }

    patch() {
        return this.send('PATCH');
    }
}

export function apiRequest(url, data) {
    return new ApiRequest(url, data);
};

Api.request = apiRequest;

export { Api };

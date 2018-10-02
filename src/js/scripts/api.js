import $ from 'jquery';
import Q from 'q';
import 'string.prototype.startswith';

import './strformat';
import './jquery.serializeObject';
import './csrf';


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

        if(!(method === 'GET' || method === 'HEAD')) {
			data = JSON.stringify(this.data);
		} else {
            data = this.data;
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
    let prefix = apiBase.format('');
    if (url.startsWith(prefix)) {
        url = url.substring(prefix.length);
    }
    return new Api(url, data);
};

Api.request = apiRequest;

export default Api;

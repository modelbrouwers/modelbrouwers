"use strict";

import Api from "./api";
import Paginator from "./paginator";

function handleError(xhr) {
    if (xhr.status === 400) {
        // bad request, validation error
        return Promise.reject(xhr.responseJSON);
    } else {
        return Promise.reject(xhr);
    }
}

class Manager {
    constructor(modelClass) {
        this.model = modelClass;
        this._objectCache = {
            _pages: {},
            _objects: {}
        };
    }

    _createObjs(raw_objects) {
        var objs = raw_objects.map(props => {
            let obj = new this.model(props);
            this._objectCache._objects[obj.id] = obj;
            return obj;
        });
        return objs;
    }

    all() {
        var self = this;
        var endpoint = self.model._meta.endpoints.list;

        return Api.request(endpoint)
            .get()
            .then(function(response) {
                var hasPagination = "count" in response;
                if (hasPagination) {
                    debugger; // TODO
                } else {
                    // response is a list of objects, so instatiate
                    return self._createObjs(response);
                }
            });
    }

    filter(filters, force_refresh = false) {
        // TODO: block until promise is resolved and return the result immediately?
        var endpoint = this.model._meta.endpoints.list;
        var self = this;
        var key = JSON.stringify(filters);
        var cached = self._objectCache[key];
        if (cached !== undefined && !force_refresh) {
            return Promise.resolve(cached);
        }
        return Api.request(endpoint, filters)
            .get()
            .then(function(response) {
                var paginator = new Paginator();
                paginator.paginate(response, filters.page);
                var objects = self._createObjs(response.results);
                objects.page_obj = paginator;
                self._objectCache[key] = objects; // cache the result
                return objects;
            });
    }

    get(filters) {
        var self = this;
        var endpoint = self.model._meta.endpoints.detail;
        if ("id" in filters) {
            // first check the local object cache
            var _obj = self._objectCache._objects[filters.id];
            if (_obj !== undefined) {
                return Promise.resolve(_obj);
            }
            endpoint = endpoint.replace(":id", filters.id);
            delete filters.id;
        }
        return Api.request(endpoint, filters)
            .get()
            .then(response => this._createObjs([response])[0]);
    }

    create(raw) {
        // map to object
        if (raw instanceof this.model) {
            let obj = raw;
            raw = {};
            for (let key in obj) {
                if (key == "id") {
                    continue;
                }
                raw[key] = obj[key];
            }
        }

        let endpoint = this.model._meta.endpoints.list;
        return Api.request(endpoint, raw)
            .post()
            .then(response => this._createObjs([response])[0], handleError);
    }
}

export default Manager;

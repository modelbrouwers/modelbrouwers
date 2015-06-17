/* Simple JavaScript Inheritance for ES 5.1
 * based on http://ejohn.org/blog/simple-javascript-inheritance/
 *  (inspired by base2 and Prototype)
 * MIT Licensed.
 * Taken from http://stackoverflow.com/a/15052240/973537
 */
(function(global) {
  "use strict";
  var fnTest = /xyz/.test(function(){xyz;}) ? /\b_super\b/ : /.*/;

  // The base Class implementation (does nothing)
  function BaseClass(){}

  // Create a new Class that inherits from this class
  BaseClass.extend = function(props) {
    var _super = this.prototype;

    // Set up the prototype to inherit from the base class
    // (but without running the init constructor)
    var proto = Object.create(_super);

    // Copy the properties over onto the new prototype
    for (var name in props) {
      // Check if we're overwriting an existing function
      proto[name] = typeof props[name] === "function" &&
        typeof _super[name] == "function" && fnTest.test(props[name])
        ? (function(name, fn){
            return function() {
              var tmp = this._super;

              // Add a new ._super() method that is the same method
              // but on the super-class
              this._super = _super[name];

              // The method only need to be bound temporarily, so we
              // remove it when we're done executing
              var ret = fn.apply(this, arguments);
              this._super = tmp;

              return ret;
            };
          })(name, props[name])
        : props[name];
    }

    // The new constructor
    var newClass = typeof proto.init === "function"
      ? proto.hasOwnProperty("init")
        ? proto.init // All construction is actually done in the init method
        : function SubClass(){ _super.init.apply(this, arguments); }
      : function EmptyClass(){};

    // Populate our constructed prototype object
    newClass.prototype = proto;

    // Enforce the constructor to be what we expect
    proto.constructor = newClass;

    // And make this class extendable
    newClass.extend = BaseClass.extend;

    return newClass;
  };

  // export
  global.Class = BaseClass;
})(this);


(function(global, $, Q, undefined){
  'use strict';

  var Options = Class.extend({
    init: function(opts) {
      // TODO: add some validation
      for (var key in opts) {
        this[key] = opts[key];
      }
    },
    // merge new endpoints with existing
    setEndpoints: function(endpoints) {
      this.endpoints = $.extend(true, this.endpoints, endpoints);
    }
  });


  var Manager = Class.extend({
    init: function(modelClass) {
      this.model = modelClass;
      this._objectCache = {
        _pages: {},
        _objects: {}
      };
    },

    _createObjs: function(raw_objects) {
      var self = this;
      var objs = raw_objects.map(function(props) {
        var obj = new self.model(props);
        self._objectCache._objects[obj.id] = obj;
        return obj;
      });
      return objs;
    },

    all: function() {
      var self = this;
      var endpoint = self.model._meta.endpoints.list;

      return Api.request(endpoint).get().then(function(response) {
        var hasPagination = 'count' in response;
        if (hasPagination) {
          debugger; // TODO
        } else { // response is a list of objects, so instatiate
          return self._createObjs(response);
        }
      });
    },

    filter: function(filters) {
      // TODO: block until promise is resolved and return the result immediately?
      var endpoint = this.model._meta.endpoints.list;
      var self = this;
      return Api.request(endpoint, filters).get().then(function(response) {
        // if (filters.page) {
        //   self._objectCache._pages[filters.page] = {
        //     count: response.count,
        //     next: response.next,
        //     previous: response.previous,
        //     num_result: response.results.length
        //   };
        // }
        return self._createObjs(response.results);
      });
    },

    get: function(filters) {
      var self = this;
      var endpoint = self.model._meta.endpoints.detail;
      if ('id' in filters) {
        // first check the local object cache
        var _obj = self._objectCache._objects[filters.id];
        if (_obj !== undefined) {
          var deferred = Q.defer();
          deferred.resolve(_obj);
          return deferred.promise;
        }
        endpoint = endpoint.replace(':id', filters.id);
        delete filters.id;
      }
      return Api.request(endpoint, filters).get().then(function(response) {
        var objs = self._createObjs([response]);
        return objs[0];
      });
    }
  });


  var Model = Class.extend({
    init: function(data) {
      for (var key in data) {
        this[key] = data[key]; // wrap all fields to make getters/setters
      }
    }
  });


  /* 'extend' the extend method */
  var ModelMeta = function(modelClass) {
    var oldExtend = modelClass.extend;
    return function(props) {
      // extract the required meta data
      if (props && props.Meta) {
        var _meta = props.Meta;
        delete props.Meta;
      } else {
        if (modelClass._meta) {
          var _meta = $.extend(true, {}, modelClass._meta);
        } else {
          throw new TypeError('The model must inherit from a model class, or provide a Meta property');
        }
      }

      // TODO check if we passed in a manager

      var Model = oldExtend.call(modelClass, props);

      // deal with the meta
      Model.Meta = _meta;
      Model._meta = new Options(_meta);
      Model.objects = new Manager(Model);

      // re-use this extend method for subclassing
      Model.extend = ModelMeta(Model);

      return Model;
    };
  };
  Model.extend = ModelMeta(Model);


  // export objects
  global.Model = Model;
  global.PonyJS = {
    Model: Model,
    Manager: Manager
  };

})(this, window.jQuery, window.Q);

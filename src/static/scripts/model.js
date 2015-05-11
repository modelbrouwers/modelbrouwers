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







var Options = Class.extend({
  init: function(opts) {
    // TODO: add some validation
    for (var key in opts) {
      this[key] = opts[key];
    }
  }
});


var Manager = Class.extend({
  init: function(modelClass) {
    this.model = modelClass;
    this._objectCache = {
      _pages: {}
    };
  },
  filter: function(filters) {
    // TODO: block until promise is resolved and return the result immediately?
    var endpoint = this.model._meta.endpoints.list;
    var self = this;
    return Api.request(endpoint, filters).get().then(function(response) {
      if (filters.page) {
        self._objectCache._pages[filters.page] = {
          count: response.count,
          next: response.next,
          previous: response.previous,
          num_result: response.results.length
        };
      }
      var objs = [];
      for (var i in response.results) {
        objs.push(new self.model(response.results[i]));
      }
      return objs;
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
    var _meta = props.Meta;
    delete props.Meta;

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

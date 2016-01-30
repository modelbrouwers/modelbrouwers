System.config({
  baseURL: "/static/",
  defaultJSExtensions: true,
  transpiler: "babel",
  babelOptions: {
    "optional": [
      "runtime",
      "optimisation.modules.system"
    ]
  },
  paths: {
    "github:*": "jspm_packages/github/*",
    "npm:*": "jspm_packages/npm/*"
  },

  map: {
    "URIjs": "npm:URIjs@1.15.1",
    "aurelia-http-client": "npm:aurelia-http-client@1.0.0-beta.1.0.1",
    "aurelia-pal": "npm:aurelia-pal@1.0.0-beta.1.0.2",
    "aurelia-pal-browser": "npm:aurelia-pal-browser@1.0.0-beta.1.0.3",
    "babel": "npm:babel-core@5.8.33",
    "babel-runtime": "npm:babel-runtime@5.8.29",
    "bootstrap": "github:twbs/bootstrap@3.3.5",
    "core-js": "npm:core-js@1.2.6",
    "css": "github:systemjs/plugin-css@0.1.13",
    "handlebars": "github:components/handlebars.js@2.0.0",
    "jquery": "github:components/jquery@2.2.0",
    "jquery-ui": "github:components/jqueryui@1.11.4",
    "js-cookie": "github:js-cookie/js-cookie@2.1.0",
    "json": "github:systemjs/plugin-json@0.1.0",
    "perfect-scrollbar": "npm:perfect-scrollbar@0.6.2",
    "ponyjs": "github:sergei-maertens/django-ponyjs@develop",
    "q": "npm:q@2.0.3",
    "string.prototype.startswith": "npm:string.prototype.startswith@0.2.0",
    "typeahead": "github:twitter/typeahead.js@0.11.1",
    "url": "github:jspm/nodelibs-url@0.1.0",
    "github:components/jqueryui@1.11.4": {
      "jquery": "github:components/jquery@2.2.0"
    },
    "github:jspm/nodelibs-assert@0.1.0": {
      "assert": "npm:assert@1.3.0"
    },
    "github:jspm/nodelibs-domain@0.1.0": {
      "domain-browser": "npm:domain-browser@1.1.4"
    },
    "github:jspm/nodelibs-events@0.1.1": {
      "events": "npm:events@1.0.2"
    },
    "github:jspm/nodelibs-path@0.1.0": {
      "path-browserify": "npm:path-browserify@0.0.0"
    },
    "github:jspm/nodelibs-process@0.1.2": {
      "process": "npm:process@0.11.2"
    },
    "github:jspm/nodelibs-url@0.1.0": {
      "url": "npm:url@0.10.3"
    },
    "github:jspm/nodelibs-util@0.1.0": {
      "util": "npm:util@0.10.3"
    },
    "github:sergei-maertens/django-ponyjs@develop": {
      "aurelia-http-client": "npm:aurelia-http-client@1.0.0-beta.1.0.1",
      "aurelia-pal-browser": "npm:aurelia-pal-browser@1.0.0-beta.1.0.3",
      "core-js": "npm:core-js@1.2.6",
      "handlebars": "github:components/handlebars.js@3.0.3",
      "jquery": "github:components/jquery@2.2.0",
      "js-cookie": "github:js-cookie/js-cookie@2.1.0",
      "json": "github:systemjs/plugin-json@0.1.0",
      "url": "github:jspm/nodelibs-url@0.1.0"
    },
    "github:twbs/bootstrap@3.3.5": {
      "jquery": "github:components/jquery@2.2.0"
    },
    "github:twitter/typeahead.js@0.11.1": {
      "jquery": "github:components/jquery@2.2.0"
    },
    "npm:URIjs@1.15.1": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:asap@2.0.3": {
      "domain": "github:jspm/nodelibs-domain@0.1.0",
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:assert@1.3.0": {
      "util": "npm:util@0.10.3"
    },
    "npm:aurelia-http-client@1.0.0-beta.1.0.1": {
      "aurelia-pal": "npm:aurelia-pal@1.0.0-beta.1.0.2",
      "aurelia-path": "npm:aurelia-path@1.0.0-beta.1",
      "core-js": "npm:core-js@1.2.6"
    },
    "npm:aurelia-pal-browser@1.0.0-beta.1.0.3": {
      "aurelia-pal": "npm:aurelia-pal@1.0.0-beta.1.0.2",
      "core-js": "npm:core-js@1.2.6"
    },
    "npm:babel-runtime@5.8.29": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:core-js@1.2.6": {
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "path": "github:jspm/nodelibs-path@0.1.0",
      "process": "github:jspm/nodelibs-process@0.1.2",
      "systemjs-json": "github:systemjs/plugin-json@0.1.0"
    },
    "npm:domain-browser@1.1.4": {
      "events": "github:jspm/nodelibs-events@0.1.1"
    },
    "npm:inherits@2.0.1": {
      "util": "github:jspm/nodelibs-util@0.1.0"
    },
    "npm:path-browserify@0.0.0": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:process@0.11.2": {
      "assert": "github:jspm/nodelibs-assert@0.1.0"
    },
    "npm:punycode@1.3.2": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:q@2.0.3": {
      "asap": "npm:asap@2.0.3",
      "pop-iterate": "npm:pop-iterate@1.0.1",
      "process": "github:jspm/nodelibs-process@0.1.2",
      "weak-map": "npm:weak-map@1.0.5"
    },
    "npm:url@0.10.3": {
      "assert": "github:jspm/nodelibs-assert@0.1.0",
      "punycode": "npm:punycode@1.3.2",
      "querystring": "npm:querystring@0.2.0",
      "util": "github:jspm/nodelibs-util@0.1.0"
    },
    "npm:util@0.10.3": {
      "inherits": "npm:inherits@2.0.1",
      "process": "github:jspm/nodelibs-process@0.1.2"
    }
  }
});

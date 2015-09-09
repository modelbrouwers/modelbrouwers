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
    // "*": "*",
    "github:*": "jspm_packages/github/*",
    "npm:*": "jspm_packages/npm/*"
  },

  map: {
    "URIjs": "npm:URIjs@1.16.0",
    "babel": "npm:babel-core@5.8.23",
    "babel-runtime": "npm:babel-runtime@5.8.20",
    "bootstrap": "github:twbs/bootstrap@3.3.5",
    "core-js": "npm:core-js@1.1.4",
    "css": "github:systemjs/plugin-css@0.1.16",
    "handlebars": "github:components/handlebars.js@2.0.0",
    "jquery": "github:components/jquery@2.1.4",
    "jquery-ui": "github:components/jqueryui@1.11.4",
    "perfect-scrollbar": "npm:perfect-scrollbar@0.6.4",
    "q": "npm:q@2.0.3",
    "string.prototype.startswith": "npm:string.prototype.startswith@0.2.0",
    "typeahead": "github:twitter/typeahead.js@0.11.1",
    "github:components/jqueryui@1.11.4": {
      "jquery": "github:components/jquery@2.1.4"
    },
    "github:jspm/nodelibs-domain@0.1.0": {
      "domain-browser": "npm:domain-browser@1.1.4"
    },
    "github:jspm/nodelibs-events@0.1.1": {
      "events": "npm:events@1.0.2"
    },
    "github:jspm/nodelibs-process@0.1.1": {
      "process": "npm:process@0.10.1"
    },
    "github:twbs/bootstrap@3.3.5": {
      "jquery": "github:components/jquery@2.1.4"
    },
    "github:twitter/typeahead.js@0.11.1": {
      "jquery": "github:components/jquery@2.1.4"
    },
    "npm:URIjs@1.16.0": {
      "process": "github:jspm/nodelibs-process@0.1.1"
    },
    "npm:asap@2.0.3": {
      "domain": "github:jspm/nodelibs-domain@0.1.0",
      "process": "github:jspm/nodelibs-process@0.1.1"
    },
    "npm:babel-runtime@5.8.20": {
      "process": "github:jspm/nodelibs-process@0.1.1"
    },
    "npm:core-js@1.1.4": {
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "process": "github:jspm/nodelibs-process@0.1.1",
      "systemjs-json": "github:systemjs/plugin-json@0.1.0"
    },
    "npm:domain-browser@1.1.4": {
      "events": "github:jspm/nodelibs-events@0.1.1"
    },
    "npm:q@2.0.3": {
      "asap": "npm:asap@2.0.3",
      "pop-iterate": "npm:pop-iterate@1.0.1",
      "process": "github:jspm/nodelibs-process@0.1.1",
      "weak-map": "npm:weak-map@1.0.5"
    }
  }
});

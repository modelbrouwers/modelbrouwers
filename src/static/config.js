System.config({
  "baseURL": "/static/",
  "transpiler": "traceur",
  "babelOptions": {
    "optional": [
      "runtime"
    ]
  },
  "paths": {
    "*": "*.js",
    "github:*": "jspm_packages/github/*.js",
    "npm:*": "jspm_packages/npm/*.js"
  }
});

System.config({
  "depCache": {
    "npm:pop-iterate@1.0.1/object-iterator": [
      "npm:pop-iterate@1.0.1/iteration",
      "npm:pop-iterate@1.0.1/array-iterator"
    ],
    "scripts/jquery.serializeObject": [
      "github:components/jquery@2.1.4"
    ],
    "scripts/csrf": [
      "github:components/jquery@2.1.4"
    ],
    "scripts/paginator": [
      "github:components/jquery@2.1.4"
    ],
    "github:components/jquery@2.1.4": [
      "github:components/jquery@2.1.4/jquery"
    ],
    "github:components/handlebars.js@2.0.0": [
      "github:components/handlebars.js@2.0.0/handlebars"
    ],
    "npm:weak-map@1.0.5": [
      "npm:weak-map@1.0.5/weak-map"
    ],
    "npm:pop-iterate@1.0.1/array-iterator": [
      "npm:pop-iterate@1.0.1/iteration"
    ],
    "npm:process@0.10.1": [
      "npm:process@0.10.1/browser"
    ],
    "scripts/api": [
      "github:components/jquery@2.1.4",
      "npm:q@2.0.3",
      "scripts/strformat",
      "scripts/jquery.serializeObject",
      "scripts/csrf"
    ],
    "github:twbs/bootstrap@3.3.5/js/bootstrap": [
      "github:components/jquery@2.1.4"
    ],
    "npm:pop-iterate@1.0.1/pop-iterate": [
      "npm:pop-iterate@1.0.1/array-iterator",
      "npm:pop-iterate@1.0.1/object-iterator"
    ],
    "github:jspm/nodelibs-process@0.1.1/index": [
      "npm:process@0.10.1"
    ],
    "scripts/manager": [
      "npm:q@2.0.3",
      "scripts/api",
      "scripts/paginator"
    ],
    "github:twbs/bootstrap@3.3.5": [
      "github:twbs/bootstrap@3.3.5/js/bootstrap"
    ],
    "npm:pop-iterate@1.0.1": [
      "npm:pop-iterate@1.0.1/pop-iterate"
    ],
    "github:jspm/nodelibs-process@0.1.1": [
      "github:jspm/nodelibs-process@0.1.1/index"
    ],
    "scripts/model": [
      "github:components/jquery@2.1.4",
      "scripts/manager"
    ],
    "npm:asap@2.0.3/browser-raw": [
      "github:jspm/nodelibs-process@0.1.1"
    ],
    "albums/js/models/photo": [
      "scripts/model"
    ],
    "npm:asap@2.0.3/asap": [
      "npm:asap@2.0.3/browser-raw",
      "github:jspm/nodelibs-process@0.1.1"
    ],
    "npm:asap@2.0.3": [
      "npm:asap@2.0.3/asap"
    ],
    "npm:q@2.0.3/q": [
      "npm:weak-map@1.0.5",
      "npm:pop-iterate@1.0.1",
      "npm:asap@2.0.3",
      "github:jspm/nodelibs-process@0.1.1"
    ],
    "npm:q@2.0.3": [
      "npm:q@2.0.3/q"
    ],
    "general/js/hbs-pony": [
      "github:components/jquery@2.1.4",
      "github:components/handlebars.js@2.0.0",
      "npm:q@2.0.3"
    ],
    "albums/js/album": [
      "github:twbs/bootstrap@3.3.5",
      "general/js/hbs-pony",
      "albums/js/models/photo"
    ],
    "albums/js/photo-detail": [
      "github:twbs/bootstrap@3.3.5"
    ]
  }
});

System.config({
  "map": {
    "URIjs": "npm:URIjs@1.15.1",
    "babel": "npm:babel-core@5.6.4",
    "babel-runtime": "npm:babel-runtime@5.6.4",
    "bootstrap": "github:twbs/bootstrap@3.3.5",
    "core-js": "npm:core-js@0.9.18",
    "css": "github:systemjs/plugin-css@0.1.13",
    "handlebars": "github:components/handlebars.js@2.0.0",
    "jquery": "github:components/jquery@2.1.4",
    "jquery-ui": "github:components/jqueryui@1.11.4",
    "perfect-scrollbar": "npm:perfect-scrollbar@0.6.2",
    "q": "npm:q@2.0.3",
    "traceur": "github:jmcriffey/bower-traceur@0.0.88",
    "traceur-runtime": "github:jmcriffey/bower-traceur-runtime@0.0.88",
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
    "npm:URIjs@1.15.1": {
      "process": "github:jspm/nodelibs-process@0.1.1"
    },
    "npm:asap@2.0.3": {
      "domain": "github:jspm/nodelibs-domain@0.1.0",
      "process": "github:jspm/nodelibs-process@0.1.1"
    },
    "npm:babel-runtime@5.6.4": {
      "process": "github:jspm/nodelibs-process@0.1.1"
    },
    "npm:core-js@0.9.18": {
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


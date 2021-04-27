const kebabcase = require("lodash.kebabcase");
const capitalize = require("lodash.capitalize");
const camelCase = require("lodash.camelcase");
const upperFirst = require("lodash.upperfirst");
const componentGenerator = require("./prompts");

module.exports = function(plop) {
    // Text tools
    plop.setHelper("kebab", function(text) {
        return kebabcase(text);
    });
    plop.setHelper("titletext", function(text) {
        return capitalize(text);
    });
    plop.setHelper("properCase", function(text) {
        return upperFirst(camelCase(text));
    });
    plop.setGenerator("component", componentGenerator);
};

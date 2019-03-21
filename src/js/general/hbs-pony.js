"use strict";

import "jquery";
import Handlebars from "handlebars/dist/handlebars.min.js";

import TemplateConsumer from "../data/hbs-template";
import { API_ROOT } from "../constants";

let hbsHelpers = [];
const consumer = new TemplateConsumer();

/**
 * @param name: name of the template, in the format app::name
 */
function renderTemplate(name, context = {}, $dest) {
    var bits = name.split("::");
    var app = bits[0],
        name = bits[1];

    return consumer.loadTemplate(app, name).then(tpl => {
        let rendered = tpl(context);
        if ($dest) {
            $dest.html(rendered);
        }
        return rendered;
    });
}
if (Handlebars.renderTemplate) {
    console.warn("Warning: overwriting renderTemplate");
}
if (Handlebars.render) {
    console.warn("Warning: overwriting render");
}
Handlebars.render = Handlebars.renderTemplate = renderTemplate;

/**
 *  Handlebars helpers
 */
var _yesno = function(bool, options) {
    var _defaults = {
        yes: '<i class="fa fa-check"></i>',
        no: '<i class="fa fa-times"></i>'
    };
    var hash = $.extend(_defaults, options.hash);
    var result;

    if (Handlebars.Utils.isFunction(bool)) {
        bool = bool.call(this);
    }

    if (!bool || Handlebars.Utils.isEmpty(bool)) {
        result = hash.no;
    } else {
        result = hash.yes;
    }
    if (Handlebars.Utils.isFunction(result)) {
        result = result.call(this);
    }
    return new Handlebars.SafeString(result);
};
hbsHelpers.push({ name: "yesno", fn: _yesno });

var _isEven = function(number, options) {
    if (number % 2 === 0) {
        return options.fn(this);
    } else {
        return options.inverse(this);
    }
};
hbsHelpers.push({ name: "if_even", fn: _isEven });

var _add = function(number, number2, options) {
    return number + number2;
};
hbsHelpers.push({ name: "add", fn: _add });

var _ifequal = function(lhs, rhs, options) {
    var equal;
    if (options.strict) {
        equal = lhs === rhs;
    } else {
        equal = lhs == rhs;
    }
    return Handlebars.helpers["if"].call(this, equal, options);
};
hbsHelpers.push({ name: "ifequal", fn: _ifequal });

var _debug = function(ctx, options) {
    console.log(ctx);
};
hbsHelpers.push({ name: "debug", fn: _debug });

let _cycle = function() {
    // spread/destructuring doesn't work like [...items, ctx] = arguments
    let ctx = Array.prototype.slice.call(arguments, -1)[0];
    let items = Array.prototype.slice.call(arguments, 0, arguments.length - 1);
    let index = ctx.data.index % items.length;
    return items[index];
};
hbsHelpers.push({ name: "cycle", fn: _cycle });

/**
 * Register the helpers
 */

hbsHelpers.forEach(function(helper, i) {
    Handlebars.registerHelper(helper.name, helper.fn);
});

export default Handlebars;

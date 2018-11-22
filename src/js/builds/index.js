"use strict";

import "jquery";

import initSearch from "./search.js";
import initBuildForm from "./build-form.js";
import KitWidget from "../kits/modelkit.widget";

export default class Page {
    static init() {
        initSearch();
        initBuildForm();
        KitWidget.init();
    }
}

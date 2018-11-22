"use strict";

import "jquery";

import initSearch from "./search.js";
import initBuildForm from "./build-form.js";

export default class Page {
    static init() {
        initSearch();
        initBuildForm();
    }
}

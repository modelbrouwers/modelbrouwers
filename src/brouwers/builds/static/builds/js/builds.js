'use strict';

import 'jquery';

import initSearch from './search.js';
import initBuildForm from './build-form.js';


$(function() {

    initSearch();
    initBuildForm();

    if (console && console.debug) {
        console.debug('Done initializing');
    }

});

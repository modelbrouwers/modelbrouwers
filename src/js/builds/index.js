'use strict';

import 'jquery';

import initBuildForm from './build-form.js';
import initSearch from './search.js';

export default class Page {
  static init() {
    initSearch();
    initBuildForm();
  }
}

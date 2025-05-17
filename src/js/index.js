import '@babel/polyfill';
import 'bootstrap';
import 'bootstrap-datepicker';
import 'bootstrap-datepicker/js/locales/bootstrap-datepicker.nl';
import 'bootstrap-select';

import {setCsrfTokenValue} from '@/data/api-client';

import './csrf';
import './fallback-img';
// components
import './kits';
import './mobile-nav';
// pages
import Router from './router/router';

const main = document.querySelector('main');
const {csrftoken} = main?.dataset;
if (csrftoken) setCsrfTokenValue(csrftoken);

// Start routing
Router.route();

// global bootstrap stuff
$('.help').popover({
  placement: 'auto right',
});

$('.badge').tooltip({
  placement: 'auto left',
});

$('td.help_text div').hide(); // hide the help texts

$('img').tooltip({
  track: true,
});

$('input.date').datepicker({
  language: 'nl',
  format: 'yyyy-mm-dd',
});
$('.selectpicker').selectpicker();

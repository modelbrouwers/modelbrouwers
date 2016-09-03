import Brand from 'kits/js/models/Brand';
import ModelKit from 'kits/js/models/ModelKit';
import {Scale, cleanScale} from 'kits/js/models/Scale';

import 'jquery';
import 'bootstrap';
import 'scripts/jquery.serializeObject';
import Handlebars from 'general/js/hbs-pony';

import {
    AddDefaultsFiller, Autocomplete,
    KitSearch, NewKitSubmitter
} from './modelkit.lib.js';


let conf = {
    prefix: '__modelkitselect',
    prefix_add: '__modelkitadd',
    htmlname: null,
    minChars: 2,
    add_modal: '#add-kit-modal',
    isMulti: false,
    typeahead: {
        brand: {
            display: 'name',
            param: 'name',
            minLength: 2
        },
        scale: {
            display: '__unicode__',
            param: 'scale',
            sanitize: cleanScale,
            minLength: 1
        },
    }
};

let checkedKits = [];


let filler = new AddDefaultsFiller(conf);
let submitter = new NewKitSubmitter(conf);


$(function() {
    let selBrand = '#id_{0}-brand'.format(conf.prefix);
    let selScale = '#id_{0}-scale'.format(conf.prefix);
    let selName = '#id_{0}-name'.format(conf.prefix);
    let $selects = $('{0}, {1}'.format(selBrand, selScale));

    let formField = document.querySelector('.model-kit-select');
    if (formField !== null) {

        // init search based on filters
        new KitSearch(conf, '.model-kit-select');

        // init
        initTypeaheads();

        // events
        $('.kit-suggestions').on('click', 'button', loadMore);

        // bind manually, because the globally included bootstrap is being annoying
        $(`[data-target="${ conf.add_modal }"]`).on('click', (e) => {
            e.preventDefault();
            $(conf.add_modal).modal('toggle');
            return false;
        });
        $(conf.add_modal)
            .on('shown.bs.modal', filler.callback.bind(filler))
            .on('click', 'button[type="submit"]', submitter.callback)
        ;
    }

});


function loadMore(event) {
    event.preventDefault();
    let $target = $(this).closest('.kit-suggestions');
    let $container = $target.siblings('[data-filters="true"]');
    let filters = getKitFilters($container);
    filters.page = $(this).data('next');
    $(this).remove(); // this shows the loader
    renderKitPreviews(filters, $target, true);
    return false;
}


function initTypeaheads() {
    let fields = conf.typeahead;
    for (let f of Object.keys(fields)) {
        new Autocomplete(f, fields[f]).initialize();
    }
}

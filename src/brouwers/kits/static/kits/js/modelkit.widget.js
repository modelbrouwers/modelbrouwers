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


let filler = new AddDefaultsFiller(conf);
let submitter = new NewKitSubmitter(conf);


$(function() {

    let formField = document.querySelector('.model-kit-select');
    if (formField !== null) {

        // init search based on filters
        let kitSearch = new KitSearch(conf, '.model-kit-select');

        // init
        for (let f of Object.keys(conf.typeahead)) {
            new Autocomplete(f, conf.typeahead[f]).initialize();
        }

        // events
        $('.kit-suggestions').on('click', 'button', kitSearch.loadMore);

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

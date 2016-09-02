import Brand from 'kits/js/models/Brand';
import ModelKit from 'kits/js/models/ModelKit';
import {Scale, cleanScale} from 'kits/js/models/Scale';

import 'jquery';
import 'bootstrap';
import 'scripts/jquery.serializeObject';
import Handlebars from 'general/js/hbs-pony';

import {
    AddDefaultsFiller, Autocomplete,
    NewKitSubmitter
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
        let dataset = formField.dataset;
        conf.isMulti = !!parseInt(dataset.allowMultiple, 10);
        conf.htmlname = dataset.htmlname;

        // init
        initTypeaheads();

        // events
        $selects.change(refreshKits);
        $(selName).keyup(refreshKits);
        $(window).resize(syncHeight);

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


function getKitFilters($container) {
    let filters = $container.serializeObject();
    let allEmpty = true;
    // strip off the prefix
    for (let key of Object.keys(filters)) {
        let newKey = key.replace('{0}-'.format(conf.prefix), '');
        filters[newKey] = filters[key];
        if (filters[key]) {
            allEmpty = false;
        }
        delete filters[key];
    }
    if (allEmpty) {
        return null;
    }
    return filters;
}


function renderKitPreviews(filters, $target, append) {
    if (filters === null) {
        $target.find('.preview').remove();
        return;
    }
    return ModelKit.objects.filter(filters).then(kits => {
        if (!kits.length) {
            $('.add-kit').show();
        }
        // read the pagination information to pass it to the template
        let page = filters.page || 1;
        // kits can actually be empty, which causes the Paginator to throw EmptyPage
        let pageObj = kits.length ? kits.paginator.page(page) : null;

        // clean up the DOM
        let previews = $target.find('.preview');

        previews.each((index, preview) => {
            let cb = $(preview).find('input[type="checkbox"]');
            let isChecked = cb && cb.is(':checked');
            if (isChecked) {
                let id = $(preview).data('id');
                if (checkedKits.indexOf(id) === -1) {
                    checkedKits.push(id);
                }
            }
        });

        if (!append) {
            previews.filter((index, preview) => {
                let id = $(preview).data('id');
                return checkedKits.indexOf(id) === -1;
            }).remove();
        } else {
            // remove any possible loaders
            previews.filter((index, preview) => {
                return $(preview).find('.fa-spinner').length > 0;
            }).remove();
        }

        // don't render the same kit again if it's in the list
        kits = kits.filter(kit => {
            return checkedKits.indexOf(kit.id) === -1;
        });
        let context = {
            isMulti: conf.isMulti,
            kits: kits,
            htmlname: conf.htmlname,
            page: {
                hasNext: pageObj ? pageObj.hasNext() : false,
                nextPageNumber: (pageObj && pageObj.hasNext()) ? pageObj.nextPageNumber() : null
            },
        };
        return Handlebars.render('kits::select-modelkit-widget', context);
    }).then(html => {
        $target.append(html);
        syncHeight();
    }).catch((error) => {
        console.error(error);
    });
}


function refreshKits(event) {
    let $container = $(this).closest('[data-filters="true"]');
    let $target = $container.siblings('.kit-suggestions');
    let filters = getKitFilters($container);

    if ($(this).is('input[type="text"]') && $(this).val() < conf.minChars && $(this).val() != '') {
        return;
    }

    renderKitPreviews(filters, $target);
}


function syncHeight() {
    let loadMore = $('.preview.center-all');
    if (!loadMore) {
        return;
    }
    loadMore.height(loadMore.prev().height());
}


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

import { Brand } from 'kits/js/models/Brand';
import { ModelKit } from 'kits/js/models/ModelKit';
import { Scale } from 'kits/js/models/Scale';

import 'jquery';
import 'scripts/jquery.serializeObject';
import 'typeahead';
import Handlebars from 'general/js/hbs-pony';


let conf = {
    prefix: '__modelkitselect',
    prefix_add: '__modelkitadd',
    htmlname: 'kits',
    minChars: 2,
    add_modal: '#add-kit-modal',
};

let checkedKits = [];

let brands = [];


$(function() {

    console.log('loaded');

    let selBrand = '#id_{0}-brand'.format(conf.prefix);
    let selScale = '#id_{0}-scale'.format(conf.prefix);
    let selName = '#id_{0}-name'.format(conf.prefix);
    let $selects = $('{0}, {1}'.format(selBrand, selScale));

    // init
    initTypeaheads();

    // events
    $selects.change(refreshKits);
    $(selName).keyup(refreshKits);
    $(window).resize(syncHeight);
    $('.kit-suggestions').on('click', 'button', loadMore);
    $(conf.add_modal).on('shown.bs.modal', fillAddDefaults);
});


function getKitFilters($container) {
    let filters = $container.serializeObject();
    let allEmpty = true;
    // strip off the prefix
    for (let key in filters) {
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
        let pageObj = kits.page_obj;
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
            kits: kits,
            htmlname: conf.htmlname,
            page: pageObj,
        };
        return Handlebars.render('kits::select-modelkit-widget', context);
    }).done(html => {
        $target.append(html);
        syncHeight();
    });
}


function refreshKits(event) {
    let $container = $(this).closest('[data-filters="true"');
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


function fillAddDefaults(event) {
    debugger;
    let fields = ['brand', 'scale'];
    let selBrand = '#id_{0}-brand'.format(conf.prefix);
    let selScale = '#id_{0}-scale'.format(conf.prefix);
    fields.forEach(field => {
        let option = $('#id_{0}-{1} option:selected'.format(conf.prefix, field));
        debugger;
        if (option) {
            let input = $('#id_{0}-{1}_ta'.format(conf.prefix_add, field));
        }
    });
}


function initTypeaheads() {
    let fields = ['brand'];
    fields.forEach(f => {

        let hiddenInput = $('#id_{0}-{1}'.format(conf.prefix_add, f));
        let input = $('#id_{0}-{1}_ta'.format(conf.prefix_add, f));

        input.typeahead(
            {
                minLength: 2,
                highlight: true
            },
            {
                async: true,
                source: ( query, sync, async ) => {

                    debugger;

                    hiddenInput.val('');
                    $.get( '/api/v1/kits/brand/', { name: query }, data => {
                        async( data );
                    });
                },
                limit: 100,
                display: 'name',
            }
        );

        input.on('typeahead:select', (event, suggestion) => {
            hiddenInput.val(suggestion.id);
        });
    });
}

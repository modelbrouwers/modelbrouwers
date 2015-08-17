import { ModelKit } from 'kits/js/models/ModelKit';

import 'jquery';
import 'scripts/jquery.serializeObject';
import Handlebars from 'general/js/hbs-pony';


let conf = {
    prefix: '__modelkitselect',
    htmlname: 'kits',
    minChars: 2,
};

let checkedKits = [];


$(function() {

    console.log('loaded');

    let selBrand = '#id_{0}-brand'.format(conf.prefix);
    let selScale = '#id_{0}-scale'.format(conf.prefix);
    let selName = '#id_{0}-name'.format(conf.prefix);
    let $selects = $('{0}, {1}'.format(selBrand, selScale));

    // events
    $selects.change(refreshKits);
    $(selName).keyup(refreshKits);
    $(window).resize(syncHeight);
    $('.kit-suggestions').on('click', 'button', loadMore);
});


function getKitFilters($container) {
    let filters = $container.serializeObject();
    // strip off the prefix
    for (let key in filters) {
        let newKey = key.replace('{0}-'.format(conf.prefix), '');
        filters[newKey] = filters[key];
        delete filters[key];
    }
    return filters;
}


function renderKitPreviews(filters, $target, append) {
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

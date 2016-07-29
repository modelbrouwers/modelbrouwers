import Brand from 'kits/js/models/Brand';
import ModelKit from 'kits/js/models/ModelKit';
import {Scale, cleanScale} from 'kits/js/models/Scale';

import 'jquery';
import 'bootstrap';
import 'scripts/jquery.serializeObject';
import 'typeahead';
import Handlebars from 'general/js/hbs-pony';


let conf = {
    prefix: '__modelkitselect',
    prefix_add: '__modelkitadd',
    htmlname: 'kits',
    minChars: 2,
    add_modal: '#add-kit-modal',
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


$(function() {
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

    // bind manually, because the globally included bootstrap is being annoying
    $(`[data-target="${ conf.add_modal }"]`).on('click', (e) => {
        e.preventDefault();
        $(conf.add_modal).modal('toggle');
        return false;
    });
    $(conf.add_modal)
        .on('shown.bs.modal', fillAddDefaults)
        .on('click', 'button[type="submit"]', submitNewKit)
    ;
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


/**
 * If the corresponding option is filled in the dropdowns, pre-select these in
 * the add-kit popup.
 */
function fillAddDefaults(event) {
    let fields = ['brand', 'scale'];
    let selBrand = '#id_{0}-brand'.format(conf.prefix);
    let selScale = '#id_{0}-scale'.format(conf.prefix);
    fields.forEach(field => {
        let sel = '#id_{0}-{1}'.format(conf.prefix, field);
        let option = $(sel).find('option:selected');
        if ($(sel).val() && option) {
            let input = $('#id_{0}-{1}_ta'.format(conf.prefix_add, field));
            if (!input.val()) {
                let hiddenInput = $('#id_{0}-{1}'.format(conf.prefix_add, field));
                hiddenInput.val(option.val());
                input.val(option.text());
            }
        }
    });
}


// FIXME: avoid submitting the same brand again
// FIXME: avoid submitting the same scale again (shows validation error)
function submitNewKit(event) {
    event.preventDefault();

    // data processing
    let modal = $(this).closest('.modal');
    let data = modal.serializeObject();
    data.stripPrefix(conf.prefix_add);
    modal.find('.errorlist').remove();

    // configuration
    let models = {
        brand: Brand,
        scale: Scale,
    };
    let brand, scale;

    // check if a brand/scale was provided, otherwise create them
    let promises = [];
    ['brand', 'scale'].forEach(field => {

        let model = models[field];
        let promise;

        if (data[field]) {
            let id = data[field];
            promise = Promise.resolve(model.objects.get({id: id}));
        } else {
            let newValue = data[`${ field }_ta`];
            let obj = $.extend(true, {}, model.fromRaw(newValue));
            delete obj._state; // not JSON serializeable, circular reference
            promise = model.objects.create(obj);
            promise.then(obj => {
                let id = obj.id;
                let display = obj[conf.typeahead[field].display];
                let select = $(`#id_${ conf.prefix }-${ field }`);
                select.append(`<option value="${ id }">${ display }</option>`);
                select.val(id);
                return obj;
            }, validationErrors => {
                let htmlField = $(`#id_${conf.prefix_add}-${field}_ta`);
                let renders = [];
                for (let fieldName of Object.keys(validationErrors.errors)) {
                    renders.push(showErrors(htmlField, validationErrors.errors[fieldName]));
                }
                return Promise.all(renders);
            });
        }
        promises.push(promise);
    });

    // create the kit with the correct data
    Promise.all(promises)
        .then(returnValues => {
            brand = returnValues[0];
            scale = returnValues[1];
            return ModelKit.objects.create({
                brand: brand.id,
                scale: scale.id,
                name: data.name
            });
        })
        .then(kit => {
            // set correct objects, different serializer used, to be implemented properly in ponyjs
            kit.brand = brand;
            kit.scale = scale;

            let context = {
                kits: [kit],
                htmlname: conf.htmlname,
                checked: true
            };

            Handlebars
                .render('kits::select-modelkit-widget', context)
                .done((html) => {
                    let $target = modal.siblings('.model-kit-select').find('.kit-suggestions');
                    let previews = $target.find('.preview');

                    if (previews) {
                        let lastChecked = previews.find('input[type="checkbox"]:checked').last().closest('.preview');
                        if (lastChecked.length) {
                            lastChecked.after(html);
                        } else {
                            $target.find('.add-kit').after(html);
                        }
                    } else {
                        $target.append(html);
                    }
                    modal.modal('toggle');
                });
        }, validationErrors => {
            // ModelKitCreate validation errors AND the first rejections validation errors
            // ignore the double display for now...
            let renders = [];
            for (let fieldName of Object.keys(validationErrors.errors)) {
                let htmlField = $(`#id_${ conf.prefix_add }-${ fieldName }`);
                renders.push(showErrors(htmlField, validationErrors.errors[fieldName]));
            }
            return Promise.all(renders);
        }).catch(error => console.error(error));
    return false;
}


function showErrors($formField, errors) {
    return Handlebars.render('general::errors', {errors: errors}).then(html => {
        $formField
            .addClass('error')
            .parent().append(html)
        ;
    });
}


function initTypeaheads() {

    let fields = conf.typeahead;

    for (let f of Object.keys(fields)) {
        let fieldConfig = fields[f];
        let _baseSelector = `#id_${ conf.prefix_add }-${ f }`;
        let hiddenInput = $(_baseSelector);
        let input = $(`${ _baseSelector }_ta`);

        let sanitize = fieldConfig.sanitize || function(query) { return query };
        let callback = `/api/v1/kits/${f}/`;

        input.typeahead(
            {
                minLength: fieldConfig.minLength,
                highlight: true
            },
            {
                async: true,
                source: (query, sync, async) => {
                    hiddenInput.val('');
                    let params = {};
                    params[fieldConfig.param] = sanitize(query);
                    $.get(callback, params, data => {
                        async(data);
                    });
                },
                limit: 100,
                display: fieldConfig.display,
            }
        );

        input.on('typeahead:select', (event, suggestion) => {
            hiddenInput.val(suggestion.id);
        });

        input.on('typeahead:render', (event, suggestion) => {
            // if we have an (case insensitive) exact match, set the value
            let $input = $(event.target);
            if (suggestion && $input.val().toLowerCase() == suggestion[fieldConfig.display].toLowerCase()) {
                hiddenInput.val(suggestion.id);
            } else {
                hiddenInput.val('');
            }
        });
    }
}

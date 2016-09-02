import 'jquery';
import 'bootstrap';
import 'scripts/jquery.serializeObject';
import 'typeahead';

import Handlebars from 'general/js/hbs-pony';

import Brand from 'kits/js/models/Brand';
import ModelKit from 'kits/js/models/ModelKit';
import Scale from 'kits/js/models/Scale';


export class AddDefaultsFiller {

    constructor(conf) {
        this.conf = conf;
    }

    callback(event) {
        let fields = ['brand', 'scale'];
        let selBrand = `#id_${this.conf.prefix}-brand`;
        let selScale = `#id_${this.conf.prefix}-scale`;

        fields.forEach(field => {
            let sel = `#id_${this.conf.prefix}-${field}`;
            let option = $(sel).find('option:selected');
            if ($(sel).val() && option) {
                let input = $(`#id_${this.conf.prefix_add}-${field}_ta`);
                if (!input.val()) {
                    let hiddenInput = $(`#id_${this.conf.prefix_add}-${field}`);
                    hiddenInput.val(option.val());
                    input.val(option.text());
                }
            }
        });
    }
}


export class NewKitSubmitter {
    constructor(conf) {
        this.conf = conf;
        this.models = {
            brand: Brand,
            scale: Scale,
        };
    }

    get callback() {
        let that = this;

        // FIXME: avoid submitting the same brand again
        // FIXME: avoid submitting the same scale again (shows validation error)
        return function(event) {
            event.preventDefault();

            // data processing
            let modal = $(this).closest('.modal');
            let data = modal.serializeObject();
            data.stripPrefix(that.conf.prefix_add);
            modal.find('.errorlist').remove();

            let brand, scale;

            // check if a brand/scale was provided, otherwise create them
            let promises = [
                that.getOrCreate('brand', data),
                that.getOrCreate('scale', data)
            ];

            // create the kit with the correct data
            Promise.all(promises)
                .then(returnValues => {
                    brand = returnValues[0];
                    scale = returnValues[1];
                    return ModelKit.objects.create({
                        brand: brand.id,
                        scale: scale.id,
                        name: data.name,
                        kit_number: data.kit_number,
                        difficulty: data.difficulty
                    });
                })
                .then(kit => {
                    // set correct objects, different serializer used, to be implemented properly in ponyjs
                    kit.brand = brand;
                    kit.scale = scale;

                    let context = {
                        isMulti: that.conf.isMulti,
                        kits: [kit],
                        htmlname: that.conf.htmlname,
                        checked: true
                    };

                    Handlebars
                        .render('kits::select-modelkit-widget', context)
                        .done(html => {
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
                        let htmlField = $(`#id_${ that.conf.prefix_add }-${ fieldName }`);
                        renders.push(showErrors(htmlField, validationErrors.errors[fieldName]));
                    }
                    return Promise.all(renders);
                }).catch(console.error);
            return false;
        }
    }

    getOrCreate(field, data) {
        let model = this.models[field];
        let promise;

        if (data[field]) {
            let id = data[field];
            promise = Promise.resolve(model.objects.get({id: id}));
        } else {
            let newValue = data[`${ field }_ta`];
            let obj = Object.assign({}, model.fromRaw(newValue));
            delete obj._state; // not JSON serializeable, circular reference
            promise = model.objects.create(obj);
            promise.then(obj => {
                let id = obj.id;
                let display = obj[this.conf.typeahead[field].display];
                let select = $(`#id_${ this.conf.prefix }-${ field }`);
                select.append(`<option value="${ id }">${ display }</option>`);
                select.val(id);
                return obj;
            }, validationErrors => {
                let htmlField = $(`#id_${this.conf.prefix_add}-${field}_ta`);
                let renders = [];
                for (let fieldName of Object.keys(validationErrors.errors)) {
                    renders.push(showErrors(htmlField, validationErrors.errors[fieldName]));
                }
                return Promise.all(renders);
            });
        }
        return promise;
    }
}


function showErrors($formField, errors) {
    return Handlebars.render('general::errors', {errors: errors}).then(html => {
        $formField
            .addClass('error')
            .parent().append(html)
        ;
    });
}


export class Autocomplete {

    /**
     * @param {String} fieldName: name of the model field to autocomplete
     * @param {Object} conf: typeahead configuration parameters:
     *     {
     *        display: {String}, field used for human readable display
     *        param: {String}, querystring parameter used for search
     *        minLength: {Number}, minimum number of characters before autocomplete kicks in
     *        sanitize(optional): {Function}, function used to clean the input
     *     }
     */
    constructor(fieldName, conf) {
        this.fieldName = fieldName;
        this.options = conf;
        this.prefix_add = '__modelkitadd';
        this.endpoint = `/api/v1/kits/${ fieldName }/`;
    }

    sanitize(query) {
        if (this.options.sanitize) {
            return this.options.sanitize(query);
        }
        return query;
    }

    initialize() {
        let _baseSelector = `#id_${ this.prefix_add }-${ this.fieldName }`;
        let hiddenInput = $(_baseSelector);
        let input = $(`${ _baseSelector }_ta`);

        input.typeahead(
            {
                minLength: this.options.minLength,
                highlight: true
            },
            {
                async: true,
                source: (query, sync, async) => {
                    hiddenInput.val('');
                    let params = {};
                    params[this.options.param] = this.sanitize(query);
                    $.get(this.endpoint, params, data => {
                        async(data);
                    });
                },
                limit: 100,
                display: this.options.display,
            }
        );

        input.on('typeahead:select', (event, suggestion) => {
            hiddenInput.val(suggestion.id);
        });

        input.on('typeahead:render', (event, suggestion) => {
            // if we have an (case insensitive) exact match, set the value
            let $input = $(event.target);
            if (suggestion && $input.val().toLowerCase() == suggestion[this.options.display].toLowerCase()) {
                hiddenInput.val(suggestion.id);
            } else {
                hiddenInput.val('');
            }
        });
    }

}

import "jquery";
import "bootstrap";
import "../scripts/jquery.serializeObject";
import "typeahead.js";
import qq from "fine-uploader";

import Handlebars from "../general/hbs-pony";

import { BrandConsumer } from "../data/kits/brand";
import { ScaleConsumer } from "../data/kits/scale";
import { ModelKitConsumer } from "../data/kits/modelkit";

/**
 * Class to handle submission of a new kit to the API.
 */
export class NewKitSubmitter {
    constructor(conf) {
        this.conf = conf;
        this.consumers = {
            brand: new BrandConsumer(),
            scale: new ScaleConsumer()
        };
        this.modal = null;
        this.boxartImageUUID = null;

        let fileinput = document.getElementById(conf.id_image_upload);
        if (fileinput) {
            this.uploader = new qq.FineUploader({
                element: fileinput.parentElement,
                request: {
                    endpoint: fileinput.dataset.endpoint,
                    inputName: "image",
                    customHeaders: {
                        "X-CSRFToken": window.csrf_token
                    }
                },
                multiple: false,
                validation: {
                    allowedExtensions: ["jpeg", "jpg", "png"] // only images
                },
                callbacks: {
                    onComplete: this.boxartImageUploaded.bind(this)
                }
            });
        }

        this.modelKitConsumer = new ModelKitConsumer();
    }

    boxartImageUploaded(id, name, responseJSON, xhr) {
        this.boxartImageUUID = responseJSON.uuid;
        let dropArea = document.querySelector(".qq-uploader__drop-area");
        dropArea.classList.add("qq-uploader__drop-area--upload-complete");

        let previews = document.querySelector(".qq-uploader__upload-list");
        previews.classList.add("qq-uploader__upload-list--upload-complete");
    }

    get callback() {
        let that = this;

        // FIXME: avoid submitting the same brand again
        // FIXME: avoid submitting the same scale again (shows validation error)
        return function(event) {
            event.preventDefault();

            // data processing
            that.modal = $(this).closest(".modal");
            let data = that.modal.serializeObject();
            data.stripPrefix(that.conf.prefix_add);
            that.modal.find(".errorlist").remove();

            let brand, scale;

            // check if a brand/scale was provided, otherwise create them
            let promises = [
                that.getOrCreate("brand", data),
                that.getOrCreate("scale", data)
            ];

            // create the kit with the correct data
            Promise.all(promises)
                .then(returnValues => {
                    brand = returnValues[0];
                    scale = returnValues[1];
                    return that.modelKitConsumer.create({
                        brand: brand.id,
                        scale: scale.id,
                        name: data.name,
                        kit_number: data.kit_number,
                        difficulty: data.difficulty,
                        box_image_uuid: that.boxartImageUUID
                    });
                })
                .then(kit => {
                    // set correct objects, different serializer used, to be implemented properly in ponyjs
                    kit.brand = brand;
                    kit.scale = scale;
                    return that.kitCreated(kit);
                })
                .catch(errors => {
                    // ModelKitCreate validation errors AND the first rejections validation errors
                    // ignore the double display for now...
                    const renders = Object.keys(errors).map(fieldName => {
                        const htmlField = $(
                            `#id_${that.conf.prefix_add}-${fieldName}`
                        );
                        return showErrors(htmlField, errors[fieldName]);
                    });

                    return Promise.all(renders);
                })
                .catch(console.error);
            return false;
        };
    }

    getOrCreate(field, data) {
        let consumer = this.consumers[field];
        let promise;

        if (data[field]) {
            let id = data[field];
            promise = Promise.resolve(consumer.read(`${id}/`)); // FIXME: append slash in consumerjs
        } else {
            let newValue = data[`${field}_ta`];
            promise = consumer
                .fromRaw(newValue)
                .then(obj => {
                    const id = obj.id;
                    const display = obj[this.conf.typeahead[field].display];
                    const select = $(`#id_${this.conf.prefix}-${field}`);
                    select.append(`<option value="${id}">${display}</option>`);
                    select.val(id);
                    return obj;
                })
                .catch(errors => {
                    const selector = `#id_${this.conf.prefix_add}-${field}_ta`;
                    const htmlField = $(selector);

                    const renders = Object.keys(errors).map(fieldName => {
                        return showErrors(htmlField, errors[fieldName]);
                    });

                    return Promise.all(renders);
                });
        }
        return promise;
    }

    kitCreated(kit) {
        let context = {
            isMulti: this.conf.isMulti,
            kits: [kit],
            htmlname: this.conf.htmlname,
            checked: true
        };

        return Handlebars.render("kits::select-modelkit-widget", context).done(
            html => {
                let $target = this.modal
                    .siblings(".model-kit-select")
                    .find(".kit-suggestions");
                let previews = $target.find(".preview");

                if (previews) {
                    let lastChecked = previews
                        .find('input[type="checkbox"]:checked')
                        .last()
                        .closest(".preview");
                    if (lastChecked.length) {
                        lastChecked.after(html);
                    } else {
                        $target.find(".add-kit").after(html);
                    }
                } else {
                    $target.append(html);
                }
                this.modal.modal("toggle");
            }
        );
    }
}

function showErrors($formField, errors) {
    return Handlebars.render("general::errors", { errors: errors }).then(
        html => {
            $formField
                .addClass("error")
                .parent()
                .append(html);
        }
    );
}

/**
 * Wrapper around TypeAhead inputs for Brand/Scale autocomplete
 */
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
        this.prefix_add = "__modelkitadd";
        this.endpoint = `/api/v1/kits/${fieldName}/`;
    }

    sanitize(query) {
        if (this.options.sanitize) {
            return this.options.sanitize(query);
        }
        return query;
    }

    initialize() {
        let _baseSelector = `#id_${this.prefix_add}-${this.fieldName}`;
        let hiddenInput = $(_baseSelector);
        let input = $(`${_baseSelector}_ta`);

        input.typeahead(
            {
                minLength: this.options.minLength,
                highlight: true
            },
            {
                async: true,
                source: (query, sync, async) => {
                    hiddenInput.val("");
                    let params = {};
                    params[this.options.param] = this.sanitize(query);
                    $.get(this.endpoint, params, data => {
                        async(data);
                    });
                },
                limit: 100,
                display: this.options.display
            }
        );

        input.on("typeahead:select", (event, suggestion) => {
            hiddenInput.val(suggestion.id);
        });

        input.on("typeahead:render", (event, suggestion) => {
            // if we have an (case insensitive) exact match, set the value
            let $input = $(event.target);
            if (
                suggestion &&
                $input.val().toLowerCase() ===
                    suggestion[this.options.display].toLowerCase()
            ) {
                hiddenInput.val(suggestion.id);
            } else {
                hiddenInput.val("");
            }
        });
    }
}

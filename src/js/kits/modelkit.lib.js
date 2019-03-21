import "jquery";
import "bootstrap";
import "../scripts/jquery.serializeObject";
import "typeahead.js";
import qq from "fine-uploader";

import Handlebars from "../general/hbs-pony";

import { BrandConsumer } from '../data/kits/brand';
import { ScaleConsumer } from '../data/kits/scale';
import { ModelKitConsumer } from '../data/kits/modelkit';


/**
 * Kit search widget implementation
 */
export class KitSearch {
    /**
     * @param {Object} conf: object holding the form prefixes and various config
     * @param {String} selector: selector for the Kit M2M/FK field (wrapper).
     */
    constructor(conf, selector) {
        this.conf = conf;
        this.node = document.querySelector(selector);
        this.checkedKits = [];
        if (this.node === null) {
            throw new Error(`No node found with selector '${selector}'`);
        }
        // update configuration
        Object.assign(this.conf, {
            isMulti: !!parseInt(this.node.dataset.allowMultiple, 10),
            htmlname: this.node.dataset.htmlname
        });
        this.bindEvents();

        this.modelKitConsumer = new ModelKitConsumer();
    }

    bindEvents() {
        // refresh the search results if a form field changes
        let ids = [
            `id_${this.conf.prefix}-brand`,
            `id_${this.conf.prefix}-scale`,
            `id_${this.conf.prefix}-name`
        ];
        let bindEvent = eventName => {
            this.node.addEventListener(eventName, event => {
                if (ids.includes(event.target.id)) {
                    this.refreshKits(event);
                }
            });
        };
        bindEvent("change");
        bindEvent("keyup");

        // fix the heights of elements if the window gets resized
        window.addEventListener("resize", this.syncLoadMoreHeight);
    }

    syncLoadMoreHeight(event) {
        let loadMore = document.querySelector(".preview.center-all");
        if (loadMore === null) {
            return;
        }
        let height = loadMore.previousElementSibling.clientHeight;
        loadMore.style.height = `${height}px`;
    }

    refreshKits(event) {
        // check for min length on text inputs
        if (
            event.target.nodeName === "INPUT" &&
            event.target.type === "text" &&
            event.target.value &&
            event.target.value.length < this.conf.minChars
        ) {
            return;
        }

        let current = event.target,
            found = false;
        let checkBool = input =>
            input === undefined ? false : !!JSON.parse(input);

        while (!found && current.parentNode) {
            found = checkBool(current.dataset.filters);
            if (found) break;
            current = current.parentNode;
        }
        if (!found) {
            console.warn("Could not find container");
        }

        // find the target div to render previews
        let target = current;
        while (
            !target.classList.contains("kit-suggestions") &&
            target.nextElementSibling
        ) {
            target = target.nextElementSibling;
        }

        this.renderKitPreviews(this.getKitFilters(current), target);
    }

    // TODO: de-jQuery-fy
    getKitFilters(node) {
        let filters = $(node).serializeObject();
        let allEmpty = true;
        // strip off the prefix
        for (let key of Object.keys(filters)) {
            let newKey = key.replace(`${this.conf.prefix}-`, "");
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

    // TODO: de-jQuery-fy
    renderKitPreviews(filters, target, append) {
        if (filters === null) {
            let node = target.querySelector(".preview");
            node !== null ? node.parentNode.removeChild(node) : null;
            return;
        }

        let $target = $(target);
        return this.modelKitConsumer
            .filter(filters)
            .then(kits => {
                if (!kits.length) {
                    $(".add-kit").show();
                }
                // read the pagination information to pass it to the template
                let page = filters.page || 1;
                // kits can actually be empty, which causes the Paginator to throw EmptyPage
                let pageObj = kits.length ? kits.paginator.page(page) : null;

                // clean up the DOM
                let previews = $target.find(".preview");

                previews.each((index, preview) => {
                    let cb = $(preview).find('input[type="checkbox"]');
                    let isChecked = cb && cb.is(":checked");
                    if (isChecked) {
                        let id = $(preview).data("id");
                        if (!this.checkedKits.includes(id)) {
                            this.checkedKits.push(id);
                        }
                    }
                });

                if (!append) {
                    previews
                        .filter((index, preview) => {
                            let id = $(preview).data("id");
                            return !this.checkedKits.includes(id);
                        })
                        .remove();
                } else {
                    // remove any possible loaders
                    previews
                        .filter((index, preview) => {
                            return $(preview).find(".fa-spinner").length > 0;
                        })
                        .remove();
                }

                // don't render the same kit again if it's in the list
                kits = kits.filter(kit => {
                    return !this.checkedKits.includes(kit.id);
                });
                let context = {
                    isMulti: this.conf.isMulti,
                    kits: kits,
                    htmlname: this.conf.htmlname,
                    page: {
                        hasNext: pageObj ? pageObj.hasNext() : false,
                        nextPageNumber:
                            pageObj && pageObj.hasNext()
                                ? pageObj.nextPageNumber()
                                : null
                    }
                };
                return Handlebars.render(
                    "kits::select-modelkit-widget",
                    context
                );
            })
            .then(html => {
                $target.append(html);
                this.syncLoadMoreHeight();
            })
            .catch(error => {
                console.error(error);
            });
    }

    // TODO: de-jQuery-fy
    loadMore(event) {
        event.preventDefault();
        let elem = $(event.target);
        let $target = elem.closest(".kit-suggestions");
        let $container = $target.siblings('[data-filters="true"]');
        let filters = this.getKitFilters($container[0]);
        filters.page = elem.data("next");
        elem.remove(); // this shows the loader
        this.renderKitPreviews(filters, $target, true);
        return false;
    }
}

/**
 * Helper class to fill the defaults from the search form fields.
 */
export class AddDefaultsFiller {
    constructor(conf) {
        this.conf = conf;
    }

    callback(event) {
        let fields = ["brand", "scale"];
        let selBrand = `#id_${this.conf.prefix}-brand`;
        let selScale = `#id_${this.conf.prefix}-scale`;

        fields.forEach(field => {
            let sel = `#id_${this.conf.prefix}-${field}`;
            let option = $(sel).find("option:selected");
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

/**
 * Class to handle submission of a new kit to the API.
 */
export class NewKitSubmitter {
    constructor(conf) {
        this.conf = conf;
        this.consumers = {
            brand: new BrandConsumer(),
            scale: new ScaleConsumer(),
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
                        const htmlField = $(`#id_${that.conf.prefix_add}-${fieldName}`);
                        return showErrors(htmlField, errors[fieldName])
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
            promise = Promise.resolve(consumer.read(`${id}/`));  // FIXME: append slash in consumerjs
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
                .catch((errors) => {
                    const selector = `#id_${this.conf.prefix_add}-${field}_ta`;
                    const htmlField = $(selector);

                    const renders = Object.keys(errors).map(fieldName => {
                        return showErrors(htmlField, errors[fieldName])
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

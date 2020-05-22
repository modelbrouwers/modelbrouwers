import { cleanScale } from "../data/kits/scale";

import "jquery";
import "bootstrap";
import "../scripts/jquery.serializeObject";

import {
    AddDefaultsFiller,
    Autocomplete,
    NewKitSubmitter
} from "./modelkit.lib.js";

let conf = {
    prefix: "__modelkitselect",
    prefix_add: "__modelkitadd",
    id_image_upload: "id___modelkitadd-box_image",
    htmlname: null,
    minChars: 2,
    add_modal: "#add-kit-modal",
    isMulti: false,
    typeahead: {
        brand: {
            display: "name",
            param: "name",
            minLength: 2
        },
        scale: {
            display: "__unicode__",
            param: "scale",
            sanitize: cleanScale,
            minLength: 1
        }
    }
};

let filler = new AddDefaultsFiller(conf);
let submitter = new NewKitSubmitter(conf);

export default class Widget {
    static init() {
        this.initKitSelect();
    }

    static initKitSelect() {
        let formField = document.querySelector(".model-kit-select");
        if (formField !== null) {
            // init
            for (let f of Object.keys(conf.typeahead)) {
                new Autocomplete(f, conf.typeahead[f]).initialize();
            }

            // bind manually, because the globally included bootstrap is being annoying
            $(`[data-target="${conf.add_modal}"]`).on("click", e => {
                e.preventDefault();
                $(conf.add_modal).modal("toggle");
                return false;
            });
            $(conf.add_modal)
                .on("shown.bs.modal", filler.callback.bind(filler))
                .on("click", 'button[type="submit"]', submitter.callback);
        }
    }
}

import { cleanScale } from "../data/kits/scale";

import { Autocomplete, NewKitSubmitter } from "./modelkit.lib.js";

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
            display: "__str__",
            param: "scale",
            sanitize: cleanScale,
            minLength: 1
        }
    }
};

let submitter = new NewKitSubmitter(conf);

const initModal = node => {
    // set up auto-complete
    for (let f of Object.keys(conf.typeahead)) {
        new Autocomplete(f, conf.typeahead[f]).initialize();
    }

    // bring up modal when button is clicked
    const selector = `[data-target="${conf.add_modal}"]`;
    $(node).on("click", selector, event => {
        event.preventDefault();
        $(conf.add_modal).modal("toggle");
        return false;
    });

    $(conf.add_modal).on("click", 'button[type="submit"]', submitter.callback);
};

export { initModal };

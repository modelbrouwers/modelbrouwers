import 'jquery';
import 'bootstrap';

import Slider from './slider.js';

import { cleanScale } from 'kits/js/models/Scale';
import {
    AddDefaultsFiller, Autocomplete,
    NewKitSubmitter
} from 'kits/js/modelkit.lib.js';


class KitreviewsNewKitSubmitter extends NewKitSubmitter {

    kitCreated(kit) {
        window.location = kit.url_kitreviews;
    }

}


class AddKitModal {

    constructor() {
        this.selector = '#add-kit-modal';
        this.triggers = $(`[data-target="${ this.selector }"]`);
        if (this.triggers.length) {
            this.initModal();
        }
        console.log('Kitreviews initialized.');
    }

    initModal() {

        let that = this;

        let conf = {
            prefix: '__modelkitselect',
            prefix_add: '__modelkitadd',
            isMulti: false,
        }

        let filler = new AddDefaultsFiller(conf);
        let submitter = new KitreviewsNewKitSubmitter(conf);

        // bind manually, because the globally included bootstrap is being annoying
        this.triggers.on('click', e => {
            e.preventDefault();
            $(that.selector).modal('toggle');
            return false;
        });

        // bind the modal submit to API calls
        $(this.selector)
            .on('shown.bs.modal', filler.callback.bind(filler))
            .on('click', 'button[type="submit"]', submitter.callback);
    }
}

// initialize everything

// slider for property ratings
new Slider('input[type="range"]');

// auto complete fields for kit modal
let brandConfig = {
    display: 'name',
    param: 'name',
    minLength: 2
};
new Autocomplete('brand', brandConfig).initialize();

let scaleConfig = {
    display: '__unicode__',
    param: 'scale',
    sanitize: cleanScale,
    minLength: 1
};
new Autocomplete('scale', scaleConfig).initialize();

// modal binding
new AddKitModal();

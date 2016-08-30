import 'jquery';
import 'bootstrap';

import Slider from './slider.js';

import {AddDefaultsFiller, NewKitSubmitter} from 'kits/js/modelkit.lib.js';


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
        let submitter = new NewKitSubmitter(conf);

        // bind manually, because the globally included bootstrap is being annoying
        this.triggers.on('click', e => {
            e.preventDefault();
            debugger;
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

new AddKitModal();

/* global beforeEach, describe, expect, fixture */

'use strict';

import Brand from 'kits/js/models/Brand';
import ModelKit from 'kits/js/models/ModelKit';
import {Scale, cleanScale} from 'kits/js/models/Scale';
import {
    AddDefaultsFiller, Autocomplete,
    KitSearch, NewKitSubmitter
} from 'kits/js/modelkit.lib.js';

describe('Add Kit', () => {

    let result, conf;


    before(function() {
        fixture.setBase('src/js_tests/kits/fixtures',)
    });


    beforeEach(() => {
        result = fixture.load('kit_add_review.html');

        conf = {
            prefix: '__modelkitselect',
            prefix_add: '__modelkitadd',
            htmlname: null,
            minChars: 2,
            add_modal: '#add-kit-modal',
            isMulti: false,
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
    });

    afterEach(() => {
        fixture.cleanup();
    });

    it('should load fixture correctly', () => {
        expect(fixture.el.firstChild).to.equal(result[0]);
    });

    describe('getKitFilters', function() {

        it('should return correct filters', ()=> {

            let kitSearch = new KitSearch(conf, '.model-kit-select');
            let node = document.querySelector('[data-filters="true"]');

            // Nothing is selected, should return null
            expect(kitSearch.getKitFilters(node)).to.be.null;

            // Select an option
            document.getElementById(`id_${conf.prefix}-brand`).value = '1';

            expect(kitSearch.getKitFilters(node)).to.not.be.null;
            expect(kitSearch.getKitFilters(node)).to.deep.equal({brand: '1', scale: '', name: ''});
        });

    });
});


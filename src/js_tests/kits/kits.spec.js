/* global beforeEach, describe, expect, fixture */

'use strict';

import View from 'kits/js/modelkit.lib.js';

describe('Test fixtures', () => {

    let result;


    before(function() {
        fixture.setBase('src/js_tests/kits/fixtures',)
    });


    beforeEach(() => {
        result = fixture.load('kit_modal.html');
    });

    afterEach(() => {
        fixture.cleanup();
    });

    it('should load fixture correctly', () => {
        expect(fixture.el.firstChild).to.equal(result[0]);
    });
});


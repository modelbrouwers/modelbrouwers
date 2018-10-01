'use strict';

import { Model } from '../../ponyjs/models.js';


class Brand extends Model('Brand', {
    Meta: {
        app_label: 'kits',
    }
}) {

    toString() {
        return 'Brand: {0}'.format(this.name);
    }

}


/**
 * Utility to create a new Brand instance from the brand name
 */
Brand.fromRaw = function(raw) {
    return new Brand({id: null, name: raw});
};


export default Brand;

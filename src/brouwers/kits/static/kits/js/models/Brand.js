'use strict';


import Model from 'scripts/model';


class Brand extends Model {
    static Meta() {
        return {
            'app_label': 'kits',
            'name': 'Brand',
            'endpoints': {
                'list': 'kits/brand/',
                'detail': 'kits/brand/:id/',
            }
        }
    }

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

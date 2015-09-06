'use strict';


import Model from 'scripts/model';


let reScale = new RegExp('1[/:]([0-9]*)');


let cleanScale = function(input) {
    if (isNaN(Number(input))) {
        let match = reScale.exec(input);
        if (match) {
            input = match[1];
        }
    }
    return input;
};


class Scale extends Model {
    static Meta() {
        return {
            'app_label': 'kits',
            'name': 'Scale',
            'endpoints': {
                'list': 'kits/scale/',
                'detail': 'kits/scale/:id/',
            }
        }
    }

    toString() {
        return 'Scale: 1/{0}'.format(this.scale);
    }
}


/**
 * Utility to create a new Brand instance from the brand name
 */
Scale.fromRaw = function(raw) {
    return new Scale({id: null, scale: cleanScale(raw)});
};


export default Scale;
export { Scale, cleanScale };

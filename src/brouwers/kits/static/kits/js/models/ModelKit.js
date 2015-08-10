'use strict';


import Model from 'scripts/model';


class ModelKit extends Model {
    static Meta() {
        return {
            'app_label': 'kits',
            'name': 'ModelKit',
            'endpoints': {
                'list': 'kits/kit/',
                'detail': 'kits/kit/:id/',
            }
        }
    }

    toString() {
        return 'ModelKit: {0}'.format(this.title);
    }
}


export { ModelKit };

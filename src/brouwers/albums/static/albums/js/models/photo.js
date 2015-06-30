'use strict';

import Model from 'scripts/model';


class Photo extends Model {
    static Meta() {
        return {
            app_label: 'albums',
            ordering: ['order'],
            endpoints: {
                list: 'albums/photo/',
                detail: 'albums/photo/:id/'
            }
        }
    }

    toString() {
        return 'Photo by {0}'.format(this.user.username);
    }

    bbcode() {
        return '[img data-id="{0}"]{1}[/img]'.format(this.id, this.image.large);
    }
}


class MyPhoto extends Photo {
    static Meta() {
        var meta = super.Meta();
        meta.endpoints = {
            list: 'my/photos/',
            detail: 'my/photos/:id/'
        }
        return meta;
    }
}


export { Photo, MyPhoto };

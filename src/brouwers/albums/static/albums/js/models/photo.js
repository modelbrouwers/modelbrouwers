'use strict';

import Api from 'scripts/api';
import Model from 'scripts/model';


class Photo extends Model {
    static Meta() {
        return {
            app_label: 'albums',
            ordering: ['order'],
            endpoints: {
                list: 'albums/photo/',
                detail: 'albums/photo/:id/',
                rotate: 'albums/photo/:id/rotate/'
            }
        }
    }

    toString() {
        return 'Photo by {0}'.format(this.user.username);
    }

    bbcode() {
        return '[photo data-id="{0}"]{1}[/photo]'.format(this.id, this.image.large);
    }

    rotate(direction) {
        var endpoint = Photo._meta.endpoints.rotate.replace(':id', this.id);
        return Api.request(endpoint, {direction: direction})
                  .patch()
                  .then(response => {
                    return Photo.objects._createObjs( [response] )[0];
                  });
    }
}


class MyPhoto extends Photo {
    static Meta() {
        var meta = super.Meta();
        meta.endpoints = {
            list: 'my/photos/',
            detail: 'my/photos/:id/',
        }
        return meta;
    }
}


export { Photo, MyPhoto };

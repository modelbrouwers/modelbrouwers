'use strict';

import Model from 'scripts/model';
import Handlebars from 'general/js/hbs-pony';
import { MyPhoto } from 'albums/js/models/photo';


class Album extends Model {

    static Meta() {
        return {
            app_label: 'albums',
            name: 'Album',
            ordering: ['order'],
            endpoints: {
                list: 'my/albums/',
                detail: 'my/albums/:id/'
            }
        }
    }

    toString() {
        return 'Album by {0}'.format(this.user.username);
    }

    renderPhotos(template, target, pagination_target) {
        return MyPhoto.objects.filter({album: this.id})
            .then(photos => {
                var ctx = {
                    album: this,
                    photos: photos
                };
                Handlebars.render('albums::pagination', {page_obj: photos.page_obj}, pagination_target).done();
                return Handlebars.render(template, ctx, target);
            });
    }

}

export { Album };
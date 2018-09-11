/**
 * This uses the proper PonyJS models. album.js is legacy.
 */
'use strict';

import { Model } from 'ponyjs/models.js';


class Album extends Model('Album', {
    Meta: {
        app_label: 'albums',
        endpoints: {
            'list': 'my/albums/',
            'detail': 'my/albums/:id/'
        }
    }
}) {
    toString() {
        return `Album by ${this.user.username}`;
    }
}


export default Album;

'use strict';

import { Model } from 'scripts/model';


class Photo extends Model {
    static Meta() {
        return {
            app_label: 'albums',
            name: 'Photo',
            ordering: ['order'],
            endpoints: {
                list: 'albums/photo/',
                detail: 'albums/photo/:id/'
            }
        }
    }
}




// var Photo = (function(Model, undefined) {

//     // initializer, named function for debug purposes
//     var photo = function(data) {
//         this._super(data);
//     };

//     var toString = function() {
//         return 'Photo by {0}'.format(this.user.username);
//     };

//     // model
//     var Photo = Model.extend({
//         Meta: {
//             app_label: 'albums',
//             name: 'Photo',
//             ordering: ['order'],
//             endpoints: {
//                 list: 'albums/photo/',
//                 detail: 'albums/photo/:id/'
//             }
//         },
//         init: photo,
//         toString: toString
//     });
//     return Photo;
// })(window.Model);


// /**
//  * Photo class that only looks up photo's from the authenticated user
//  */
// var MyPhoto = (function(Photo, undefined) {
//     'use strict';

//     var MyPhoto = Photo.extend();
//     MyPhoto._meta.setEndpoints({
//         list: 'my/photos/',
//         detail: 'my/photos/:id/'
//     });
//     return MyPhoto;

// })(Photo);


export { Photo };

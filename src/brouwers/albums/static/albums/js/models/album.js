var Album = (function($, Model, Api, hbs, undefined) {
    'use strict';

    // initializer, named function for debug purposes
    var album = function(data) {
        this._super(data);
    };

    var toString = function() {
        return 'Album by {0}'.format(this.user.username);
    };

    var renderPhotos = function(template, target, pagination_target) {
        var self = this;
        return MyPhoto.objects.filter({album: self.id})
            .then(function(photos) {
                var ctx = {
                    album: self,
                    photos: photos
                };

                var page_obj = {
                    number: 1, // current page
                    has_previous: true,
                    previous_page_number: 1,
                    has_next: true,
                    next_page_number: 100,
                    page_range: [1, 2, 3, 4, 5, 100]
                };

                hbs.render('albums::pagination', {page_obj: page_obj}, pagination_target).done();
                return hbs.render(template, ctx, target);
            });
    };

    // model
    var Album = Model.extend({
        Meta: {
            app_label: 'albums',
            name: 'Album',
            ordering: ['order'],
            endpoints: {
                list: 'my/albums/',
                detail: 'my/albums/:id/'
            }
        },
        init: album,
        toString: toString,
        renderPhotos: renderPhotos
    });
    return Album;
})(window.jQuery, window.Model, window.Api, window.Handlebars);

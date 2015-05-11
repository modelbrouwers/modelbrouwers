var Photo = (function($, Model, Api, undefined) {
    'use strict';

    // initializer, named function for debug purposes
    var photo = function(data) {
        this._super(data);
    };

    // model
    var Photo = Model.extend({
        Meta: {
            app_label: 'albums',
            name: 'Photo',
            ordering: ['order'],
            endpoints: {
                list: 'albums/photo/',
                detail: 'albums/photo/:id/'
            }
        },
        init: photo
    });
    return Photo;
})(window.jQuery, window.Model, window.Api);

var Photo = (function($, Model, Api, undefined) {
    'use strict';

    // initializer, named function for debug purposes
    var photo = function(data) {
        this._super(data);
    };

    // model
    var Photo = Model.extend({
        init: photo
    });

    var photos = Photo.objects.filter({album: window.album, page: window.page});

    return Photo;
})(window.jQuery, window.Model, window.Api);

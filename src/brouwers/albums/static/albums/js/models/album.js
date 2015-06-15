var Album = (function($, Model, Api, undefined) {
    'use strict';

    // initializer, named function for debug purposes
    var album = function(data) {
        this._super(data);
    };

    var toString = function() {
        return 'Album by {0}'.format(this.user.username);
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
        toString: toString
    });
    return Album;
})(window.jQuery, window.Model, window.Api);

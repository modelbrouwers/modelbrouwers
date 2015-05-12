$(function() {
    'use strict';

    var $lightbox = $('#modal-lightbox'),
        $lightboxBody = $lightbox.find('.modal-content');

    $('#photo-thumbs').on('click', '.album-photo', function(event) {
        event.preventDefault();

        var id = $(this).data('id');

        /* Closure to render the current photo in the lightbox */

        var renderLightbox = function(currentID, photos) {
            debugger;
            var context = {
                photos: photos
            };
            Handlebars.render('albums::photo-lightbox', context, $lightboxBody);
            $lightbox.modal('show');
        };



        function getLightboxRenderer(id) {
            var currentID = id;
            return function(photos) {
                debugger;
                return renderLightbox.call(null, currentID, photos);
            };
        }


        Photo.objects.filter({
            page: window.page,
            album: window.album
        }).done(getLightboxRenderer(id));

    });

});

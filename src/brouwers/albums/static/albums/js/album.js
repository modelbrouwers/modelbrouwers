$(function() {

    $('#photo-thumbs').on('click', '.album-photo', function(event) {
        event.preventDefault();

        Photo.objects.filter({
            page: window.page,
            album: window.album,
        }).done(function(photos) {
            Handlebars.render('albums::photo-lightbox', {photos: photos}, $('#modal-lightbox .modal-body'));
            $('#modal-lightbox').modal('show');
        });

    });

});

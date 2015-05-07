$(function() {

    $('#photo-thumbs').on('click', '.album-photo', function(event) {
        event.preventDefault();

        var photos = Photo.objects.filter({
            page: window.page,
            album: window.album,
        });

        $('#modal-lightbox').modal('show');
    });

});

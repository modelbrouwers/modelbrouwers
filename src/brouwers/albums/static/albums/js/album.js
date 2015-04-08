$(function() {

    $('#photo-thumbs').on('click', '.album-photo', function(event) {
        event.preventDefault();
        $('#modal-lightbox').modal('show');
    });

});

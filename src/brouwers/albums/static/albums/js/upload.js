$(function(){
    'use strict';

    var uploader = $('#uploader');
    var albumChooser = $('#carousel-album');
    var album;

    uploader.fineUploader({
        request: {
            endpoint: endpoint,
            inputName: 'image',
            filenameParam: 'description',
            customHeaders: {
                Accept: 'text/plain', // otherwise DRF complains
                'X-CSRFToken': window.csrf_token
            }
        },
        retry: {
           enableAuto: false,
        },
        validation: {
            allowedExtensions: ['jpeg', 'jpg', 'gif', 'png'] // only images
        },
        autoUpload: autoUpload
    }).on('allComplete', function(event, succeeded, failed) {
        if (failed.length === 0) {
            window.location = decodeURI(window.albumDetail).format(album);
        }
    }).on('submit', function(event, id, name) {
        var ok = setAlbum();
        if (ok) {
            var $dest = $('#upload-form');
            $('html, body').animate({
                scrollTop: $dest.offset().top
            }, 500);
        }
        return ok;
    });

    var setAlbum = function() {
        var checked = $('#upload-form input[name="album"]:checked');
        if (checked.length !== 1) {
            $('#modal-albums').modal('show');
            return false;
        }

        album = parseInt(checked.val(), 10);
        uploader.fineUploader('setParams', {album: album});
        return true;
    };

    $('.cancel').click(function(e) {
        uploader.fineUploader('cancel', id);
    });

    $('#trigger-upload').click(function(e) {
        e.preventDefault();
        // TODO: multi upload
        setAlbum();
        uploader.fineUploader('uploadStoredFiles');
        return false;
    });

    var focusActiveAlbum = function() {
        var checked = albumChooser.find('input:checked').next();
        var hasChecked = checked.length == 1;
        while (hasChecked && !checked.is(':visible')) {
            albumChooser.carousel('next');
        }
    };
    focusActiveAlbum();
});

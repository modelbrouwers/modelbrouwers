'use strict';

import 'jquery';
import 'bootstrap';

import Album from 'albums/js/models/album2.js';
import Photo from 'albums/js/models/photo2.js';
import Handlebars from 'general/js/hbs-pony';


let conf = {
    input_url: '.formset-form input[type="url"]',
    empty_build_photo: '.formset-form',
    photo_picker: {
        picker: '#photo-picker',
        body: '#carousel-album .carousel-inner',
        list: '#photo-picker .photo-list',
    }
}


let showPhotos = function(event) {
    if (!$(this).is(':checked')) {
        return;
    }

    // reset other checkboxes
    $(conf.photo_picker.body).find('input[type="checkbox"]:checked').not(this).prop('checked', false);

    let albumId = parseInt($(this).val(), 10);

    let getQueryset = function(page=1) {
        return Photo.objects.filter({album: albumId, page: page});
    };
    /**
     * fetch the first page of photos, and figure out how many extra pages there are.
     * If more pages exist, fetch all of them and wait for all of them to complete.
     */
    getQueryset().then(photos => {
        let promises,
            page_range = photos.paginator.page_range;
        if (page_range.length > 1) {
            promises = page_range.slice(1).map(p => getQueryset(p));
        } else {
            promises = [Promise.resolve(photos)];
        }
        return Promise.all(promises);
    }).then(photo_lists => {
        let photos = [];
        photo_lists.forEach(_photos => photos.push(..._photos));
        return Handlebars.render('builds::album-photo-picker', {photos: photos});
    }).then(html => {
        $(conf.photo_picker.list).html(html);
    }).catch(e => {
        throw e;
    });
};


let showPreview = function($form, url) {
    let $preview = $form.find('.preview');
    $preview.addClass('hidden'); // always hide, only show when real urls work

    let img = new Image();
    img.onload = function() {
        $form.find('img').attr('src', url);
        $preview.removeClass('hidden');
    };
    img.src = url; // trigger loading
}


let previewUrl = function(event) {
    let url = $(this).val();
    let $form = $(this).closest('.formset-form');
    let $img = $form.find('img');
    showPreview($form, url);
};


let loadAlbums = function() {
    // endpoint without pagination
    Album.objects.all().then(albums => {
        return Handlebars.render('albums::carousel-picker', {'albums': albums});
    }).then(html => {
        // render carousel body
        $(conf.photo_picker.body).html(html);
    }).catch(e => {
        throw e;
    });
};


let addRemoveAlbumPhoto = function(event) {
    let photoId = $(this).data('id');
    let add = $(this).is(':checked');

    if (add) {
        // find candidate for formset
        let $form;
        let formset_forms = $(conf.empty_build_photo).filter((i, form) => {
            let $form = $(form);
            let inputs = $form.find('input').length;
            let emptyInputs = $form.find('input:empty').length;
            return inputs == emptyInputs;
        });
        if (formset_forms.length) {
            $form = formset_forms.first();
            $form.find('input.photo').val(photoId);
        } else {
            // add formset row, set $form
            debugger;
        }
        let url = $(this).siblings('label').find('img').data('large');
        showPreview($form, url);
    } else {
        debugger;
    }
};


$(function() {

	$('fieldset').on('change, keyup', conf.input_url, previewUrl);

    $(conf.photo_picker.body).on('change', 'input[type="checkbox"]', showPhotos);

    $(conf.photo_picker.list).on('change', 'input[type="checkbox"]', addRemoveAlbumPhoto);

    loadAlbums();
});

'use strict';

import 'jquery';
import 'bootstrap';

import Formset from 'ponyjs/forms/formsets.js';

import Album from 'albums/js/models/album2.js';
import Photo from 'albums/js/models/photo2.js';
import Handlebars from 'general/js/hbs-pony';


let conf = {
    input_url: '.formset-form input[type="url"]',
    formset: '.formset-form',
    photo_picker: {
        picker: '#photo-picker',
        add_url: '#add-url-photo',
        body: '#carousel-album .carousel-inner',
        list: '#photo-picker .photo-list',
    }
}


class PhotoFormset extends Formset {
    get template() {
        if (!this._template) {
            this._template = $('#empty-form').html();
        }
        return this._template;
    }
}


let photoFormset = new PhotoFormset('photos');


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


let showPhotos = function(event) {
    // always show the loader first
    $(conf.photo_picker.list).removeClass('hidden');
    Handlebars.render('general::loader', {}, $(conf.photo_picker.list));

    if (!$(this).is(':checked')) {
        $(conf.photo_picker.list).addClass('hidden');
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


let togglePhotoPicker = function(event) {
    event.preventDefault();
    $($(this).data('target')).toggleClass('hidden');
    return false;
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


let photoFormMapping = {};


let addRemoveAlbumPhoto = function(event) {
    let photoId = $(this).data('id');
    let add = $(this).is(':checked');

    if (add) {
        let [html, index] = photoFormset.addForm();
        $(conf.formset).closest('fieldset').append(html);
        let $form = $(conf.formset).last();
        photoFormMapping[photoId] = $form;
        $form.find('.url').hide();
        photoFormset.setData(index, {'photo': photoId});
        let url = $(this).siblings('label').find('img').data('large');
        $form.find('[data-toggle="popover"]').popover();
        showPreview($form, url);
    } else {
        let $form = photoFormMapping[photoId];
        $form.remove();
    }
};


let addUrlForm = function(event) {
    event.preventDefault();
    let [html, index] = photoFormset.addForm();
    $(conf.formset).closest('fieldset').append(html);
    let $form = $(conf.formset).last();
    $form.find('.album').hide();
    $(window, 'body').scrollTop($form.position().top);
    $form.find('input:visible').focus();
    $form.find('[data-toggle="popover"]').popover();
    return false;
};

// either show album or url, depending on which one is entered
let showAlbumOrUrls = function() {
    $(conf.formset).each((i, form) => {
        let $form = $(form);
        let prefix = `id_photos-${i}`;
        let photo = $(form).find(`#${prefix}-photo`).val();
        if (photo !== undefined) {
            $form.find('.url').hide();
        } else {
            $form.find('.album').hide();
        }
    });
};


$(function() {

    // bind change handler + trigger to display url previews
	$('fieldset').on('change, keyup', conf.input_url, previewUrl);
    $(`fieldset ${conf.input_url}`).change();

    // bind photo picker events
    $(conf.photo_picker.body).on('change', 'input[type="checkbox"]', showPhotos);
    $(conf.photo_picker.list).on('change', 'input[type="checkbox"]', addRemoveAlbumPhoto);
    $(`[data-target="${conf.photo_picker.picker}"]`).on('click', togglePhotoPicker)

    // bind trigger to add a url form
    $(conf.photo_picker.add_url).on('click', addUrlForm);

    // properly display the formset forms, if any
    showAlbumOrUrls();

    // start loading the albums
    loadAlbums();
});

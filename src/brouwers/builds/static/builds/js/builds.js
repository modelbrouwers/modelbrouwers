'use strict';

import 'jquery';
import 'bootstrap';

import Album from 'albums/js/models/album2.js';
import Handlebars from 'general/js/hbs-pony';


let conf = {
    input_url: '.formset-form input[type="url"]',
    photo_picker: '#photo-picker',
    photo_picker_body: '#carousel-album .carousel-inner',
}


$(function() {

	$('fieldset').on('change, keyup', conf.input_url, previewUrl);

    loadAlbums();
});


let previewUrl = function(event) {
    let url = $(this).val();
    let $form = $(this).closest('.formset-form');
    let $img = $form.find('img');
    let $preview = $form.find('.preview');
    $preview.addClass('hidden'); // always hide, only show when real urls work

    let img = new Image();
    img.onload = function() {
        $form.find('img').attr('src', url);
        $preview.removeClass('hidden');
    };
    img.src = url; // trigger loading
};

function loadAlbums() {
    // endpoint without pagination
    Album.objects.all().then(albums => {
        return Handlebars.render('albums::carousel-picker', {'albums': albums});
    }).then(html => {
        // render carousel body
        $(conf.photo_picker_body).html(html);
    }).catch(e => {
        throw e;
    });
};

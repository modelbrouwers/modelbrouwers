'use strict';

import 'jquery';
import 'bootstrap';
import 'scripts/jquery.insertAtCaret';
import Ps from 'perfect-scrollbar';

import Handlebars from 'general/js/hbs-pony';
import { Album } from 'albums/js/models/album';
import { MyPhoto } from 'albums/js/models/photo';


let conf = {
	selectors: {
		root: 'body.forum',
        root_sidebar: '#photo-sidebar',
		photo_list: '#photo-list',
		albums_select: 'select[name="album"]',
		pagination: '#photo-list-pagination',
        loader: '#image-loader',
        photo: '.album-photo',
        post_textarea: 'textarea[name="message"]'
	}
};

let updateScrollbar = function() {
    let $sidebar = $(conf.selectors.root_sidebar);
    Ps.update($sidebar[0]);
};


let renderSidebar = function(albums) {
	return Handlebars
		.render('albums::forum-sidebar', {albums:albums})
		.then(html => {
			$('body').append(html);

            let $sidebar = $(conf.selectors.root_sidebar);
            Ps.initialize($sidebar[0]);

			if (albums.length === 0) {
				return null;
			}
			return albums[0];
		});
};

let renderAlbumPhotos = function(album) {
    if (album === null) {
        return;
    }
    var target = $(conf.selectors.photo_list);
    var pagination_target = $(conf.selectors.pagination);
    return album
        .renderPhotos('albums::forum-sidebar-photos', target, pagination_target)
        .done(html => {
            $(conf.selectors.loader).hide();
            updateScrollbar();
        });
};

let showSidebar = function() {
    Album.objects.all()
        .then(renderSidebar)
        .done(renderAlbumPhotos);
};

let onAlbumSelectChange = function(event) {
    var id = parseInt($(this).val(), 10);
    $(conf.selectors.loader).show();
    Album.objects.get({id: id}).done(renderAlbumPhotos);
};

let insertPhotoAtCaret = function(event) {
    event.preventDefault();
    let id = $(this).data('id');
    MyPhoto.objects.get({id: id}).done(photo => {
        let $textarea = $(conf.selectors.post_textarea);
        $textarea.insertAtCaret(photo.bbcode() + "\n");
    });
    return false;
};


$(function() {
    // check if we're in posting mode
    if ($(conf.selectors.post_textarea).length == 1) {
        showSidebar();
    }

    $(conf.selectors.root)
        .on('click', '[data-open], [data-close]', function() {
            var selector = $(this).data('open') || $(this).data('close');
            $(selector).toggleClass('open closed');
            updateScrollbar();
        })
        .on('change', conf.selectors.albums_select, onAlbumSelectChange)
        .on('click', conf.selectors.photo, insertPhotoAtCaret)
    ;
});

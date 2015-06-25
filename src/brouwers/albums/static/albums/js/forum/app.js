'use strict';

import 'jquery';
import 'bootstrap';
import 'scripts/jquery.insertAtCaret';

import Handlebars from 'general/js/hbs-pony';
import { Album } from 'albums/js/models/album';
import { Photo } from 'albums/js/models/photo';


let conf = {
	selectors: {
		root: 'body.forum',
		photo_list: '#photo-list',
		albums_select: 'select[name="album"]',
		pagination: '#photo-list-pagination'
	}
};


let renderSidebar = function(albums) {
	return Handlebars
		.render('albums::forum-sidebar', {albums:albums})
		.then(html => {
			$('body').append(html);
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
        .renderPhotos('albums::forum-sidebar-photos', target, pagination_target);
};

let showSidebar = function() {
    Album.objects.all()
        .then(renderSidebar)
        .done(renderAlbumPhotos);
};

let onAlbumSelectChange = function(event) {
    var id = parseInt($(this).val(), 10);
    Album.objects.get({id: id}).done(renderAlbumPhotos);
};


$(function() {
    // check if we're in posting mode
    if ($('textarea[name="message"]').length == 1) {
        showSidebar();
    }

    $(conf.selectors.root)
        .on('click', '[data-open], [data-close]', function() {
            var selector = $(this).data('open') || $(this).data('close');
            $(selector).toggleClass('open closed');
        })
        .on('change', conf.selectors.albums_select, onAlbumSelectChange)
    ;
});

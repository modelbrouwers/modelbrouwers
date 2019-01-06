import insertTextAtCursor from 'insert-text-at-cursor';
import Ps from "perfect-scrollbar";

import Handlebars from "../general/hbs-pony";
import { Album } from "../albums/models/album";
import { MyPhoto } from "../albums/models/photo";

let conf = {
    selectors: {
        root: "body.forum",
        root_sidebar: "#photo-sidebar",
        photo_list: "#photo-list",
        albums_select: 'select[name="album"]',
        pagination: "#photo-list-pagination",
        page_link: "#photo-list-pagination .pagination a",
        loader: "#image-loader",
        photo: ".album-photo",
        post_textarea: 'textarea[name="message"],textarea[name="signature"]'
    }
};

let updateScrollbar = function() {
    let sidebar = document.querySelector(conf.selectors.root_sidebar);
    Ps.update(sidebar);
};

let renderSidebar = function(albums) {
    return Handlebars.render("albums::forum-sidebar", { albums: albums }).then(
        html => {
            let body = document.querySelector('body');
            body.insertAdjacentHTML('beforeend', html);

            let sidebar = document.querySelector(conf.selectors.root_sidebar);
            Ps.initialize($sidebar);

            if (albums.length === 0) {
                return null;
            }
            return albums[0];
        }
    );
};

let renderAlbumPhotos = function(album, page) {
    if (album === null) {
        return;
    }
    var target = $(conf.selectors.photo_list);
    var pagination_target = $(conf.selectors.pagination);
    var filters = page ? { page: page } : {};
    return album
        .renderPhotos(
            "albums::forum-sidebar-photos",
            target,
            pagination_target,
            filters
        )
        .done(html => {
            $(conf.selectors.loader).hide();
            updateScrollbar();
        });
};

let showSidebar = function() {
    Album.objects
        .all()
        .done(renderAlbumPhotos);
};

let onAlbumSelectChange = function(event) {
    var id = parseInt($(this).val(), 10);
    $(conf.selectors.loader).show();
    Album.objects.get({ id: id }).done(renderAlbumPhotos);
};

let insertPhotoAtCaret = function(event) {
    event.preventDefault();
    let id = $(this).data("id");
    MyPhoto.objects.get({ id: id }).done(photo => {
        let textarea = document.querySelector(conf.selectors.post_textarea);
        insertTextAtCursor(textAreas, photo.bbcode() + "\n");
    });
    return false;
};

let loadPage = function(event) {
    event.preventDefault();
    let page = $(this).data("page");
    let id = $(conf.selectors.albums_select).val();

    // show spinner
    $(this).html('<i class="fa fa-spin fa-spinner"></i>');

    Album.objects.get({ id: id }).done(album => {
        renderAlbumPhotos(album, page);
    });
    return false;
};


export default class App {
    static init() {
        // check if we're in posting mode
        const textAreas = document.querySelectorAll(conf.selectors.post_textarea);
        if (textAreas.length == 1) {
            renderSidebar([]);
            showSidebar();
        }

        $(conf.selectors.root)
            .on("click", "[data-open], [data-close]", function() {
                var selector = $(this).data("open") || $(this).data("close");
                $(selector).toggleClass("open closed");
                updateScrollbar();
            })
            .on("change", conf.selectors.albums_select, onAlbumSelectChange)
            .on("click", conf.selectors.photo, insertPhotoAtCaret)
            .on("click", conf.selectors.page_link, loadPage);
    }
}

import insertTextAtCursor from 'insert-text-at-cursor';
import PerfectScrollbar from "perfect-scrollbar";

import Handlebars from "../general/hbs-pony";
import { AlbumConsumer } from '../data/albums/album';
import { MyPhotoConsumer } from '../data/albums/photo';

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

const myPhotoConsumer = new MyPhotoConsumer();
const albumConsumer = new AlbumConsumer();

// module level variable until we properly refactor...
let ps;

let renderSidebar = albums => {
    return Handlebars.render("albums::forum-sidebar", { albums: albums }).then(
        html => {
            let body = document.querySelector('body');
            body.insertAdjacentHTML('beforeend', html);

            let sidebarContainer = document.querySelector(conf.selectors.root_sidebar);
            ps = new PerfectScrollbar(sidebarContainer);

            if (albums.length === 0) {
                return null;
            }
            return albums[0];
        }
    );
};

let renderAlbumPhotos = function(album, page) {
    if (album == null) {
        return;
    }

    var target = $(conf.selectors.photo_list);
    var pagination_target = $(conf.selectors.pagination);
    var filters = page ? { page: page } : {};

    return album
        .getPhotos()
        .then(photos => {
            // FIXME TODO: extract page object/pagination information!
            Handlebars.render(
                "albums::pagination",
                { page_obj: photos.page_obj },
                pagination_target
            )
            .catch(console.error);
            return Handlebars
                .render("albums::forum-sidebar-photos", { album, photos }, target);
        })
        .then(() => {
            $(conf.selectors.loader).hide();
            ps.update();
        })
        .catch(console.error);
};

let showSidebar = function() {
    albumConsumer
        .list()
        .then(renderAlbumPhotos)
        .catch(console.error);
};

let onAlbumSelectChange = function(event) {
    var id = parseInt($(this).val(), 10);
    $(conf.selectors.loader).show();

    albumConsumer
        .read(id)
        .then(renderAlbumPhotos)
        .catch(console.error);
};

let insertPhotoAtCaret = function(event) {
    event.preventDefault();
    let id = $(this).data("id");

    myPhotoConsumer
        .read(id)
        .then(photo => {
            let textarea = document.querySelector(conf.selectors.post_textarea);
            insertTextAtCursor(textAreas, photo.bbcode + "\n");
        })
        .catch(console.error);

    return false;
};

let loadPage = function(event) {
    event.preventDefault();
    let page = $(this).data("page");
    let id = $(conf.selectors.albums_select).val();

    // show spinner
    $(this).html('<i class="fa fa-spin fa-spinner"></i>');

    albumConsumer
        .read(id)
        .then(album => {
            renderAlbumPhotos(album, page);
        })
        .catch(console.error);
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
                ps.update();
            })
            .on("change", conf.selectors.albums_select, onAlbumSelectChange)
            .on("click", conf.selectors.photo, insertPhotoAtCaret)
            .on("click", conf.selectors.page_link, loadPage);
    }
}

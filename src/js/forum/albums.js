import insertTextAtCursor from "insert-text-at-cursor";
import PerfectScrollbar from "perfect-scrollbar";
import React from "react";
import ReactDOM from "react-dom";
import { IntlProvider } from "react-intl";

import { getLocale, getMessages } from "../translations/utils";
import SideBar from "./albums/SideBar";

import Paginator from "../scripts/paginator";
import Handlebars from "../general/hbs-pony";
import { AlbumConsumer } from "../data/albums/album";
import { MyPhotoConsumer } from "../data/albums/photo";

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

// module level variables until we properly refactor...
let ps;

let renderSidebar = albums => {
    return Handlebars.render("albums::forum-sidebar", { albums: albums }).then(
        html => {
            let body = document.querySelector("body");
            body.insertAdjacentHTML("beforeend", html);

            let sidebarContainer = document.querySelector(
                conf.selectors.root_sidebar
            );
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
        .getPhotos(filters)
        .then(photosResponse => {
            let photos = photosResponse.results;

            // TODO: use consumerjs pagination
            let paginator = new Paginator();
            paginator.paginate(photosResponse, page);

            Handlebars.render(
                "albums::pagination",
                { page_obj: paginator },
                pagination_target
            ).catch(console.error);

            return Handlebars.render(
                "albums::forum-sidebar-photos",
                { album, photos },
                target
            ).catch(console.error);
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
        .then(renderSidebar)
        .then(renderAlbumPhotos)
        .catch(console.error);
};

let onAlbumSelectChange = function(event) {
    var id = parseInt($(this).val(), 10);
    $(conf.selectors.loader).show();

    albumConsumer
        .read(`${id}/`)
        .then(renderAlbumPhotos)
        .catch(console.error);
};

let insertPhotoAtCaret = function(event) {
    event.preventDefault();
    let id = $(this).data("id");

    myPhotoConsumer
        .read(`${id}/`)
        .then(photo => {
            let textArea = document.querySelector(conf.selectors.post_textarea);
            insertTextAtCursor(textArea, photo.bbcode + "\n");
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
        .read(`${id}/`)
        .then(album => {
            renderAlbumPhotos(album, page);
        })
        .catch(console.error);
    return false;
};

export default class App {
    static init() {
        // check if we're in posting mode
        const textArea = document.querySelectorAll(
            conf.selectors.post_textarea
        );
        if (!textArea.length) return;

        const mountNode = document.createElement("div");
        document.body.appendChild(mountNode);

        const locale = getLocale() || "nl";
        const messages = getMessages(locale);

        ReactDOM.render(
            <IntlProvider locale={locale} messages={messages}>
                <SideBar />
            </IntlProvider>,
            mountNode
        );

        // $(conf.selectors.root)
        //     .on("click", "[data-open], [data-close]", function() {
        //         var selector = $(this).data("open") || $(this).data("close");
        //         $(selector).toggleClass("open closed");
        //         ps.update();
        //     })
        //     .on("change", conf.selectors.albums_select, onAlbumSelectChange)
        //     .on("click", conf.selectors.photo, insertPhotoAtCaret)
        //     .on("click", conf.selectors.page_link, loadPage);
    }
}

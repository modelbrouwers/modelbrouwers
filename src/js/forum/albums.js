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
        post_textarea: 'textarea[name="message"],textarea[name="signature"]',
    },
};

const myPhotoConsumer = new MyPhotoConsumer();
const albumConsumer = new AlbumConsumer();

// module level variables until we properly refactor...
let ps;

let insertPhotoAtCaret = function (event) {
    event.preventDefault();
    let id = $(this).data("id");

    myPhotoConsumer
        .read(`${id}/`)
        .then((photo) => {
            let textArea = document.querySelector(conf.selectors.post_textarea);
            insertTextAtCursor(textArea, photo.bbcode + "\n");
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
        //     .on("click", conf.selectors.photo, insertPhotoAtCaret)
    }
}

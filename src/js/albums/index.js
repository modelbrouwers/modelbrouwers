import React from "react";
import ReactDOM from "react-dom";

import "jquery";
import { MyPhotoConsumer } from "../data/albums/photo";
import { RotateControl, Control } from "./photo-detail";
import { PhotoUpload } from "./upload";
import LightBox from "./LightBox";

const myPhotoConsumer = new MyPhotoConsumer();

const setCover = (photoNode) => {
    const photoId = photoNode.dataset.id;
    const promise = myPhotoConsumer.setAsCover(photoId);
    promise
        .then(() => {
            $(".cover").removeClass("cover");
            photoNode.classList.add("cover");
        })
        .catch(console.error);
};

export default class Page {
    static init() {
        this.initLightbox();
        this.initControls();
        new PhotoUpload();
        this.initPhotoEdit();
    }

    static initLightbox() {
        const lightBox = document.getElementById("modal-lightbox");
        if (!lightBox) return;
        const targetNode = lightBox.querySelector(".modal-content");

        const thumbs = document.querySelectorAll("#photo-thumbs .album-photo");
        if (!thumbs.length) return;

        const { album, page } = lightBox.dataset;

        for (const thumb of thumbs) {
            thumb.addEventListener("click", (event) => {
                event.preventDefault();
                const { id: photoId } = event.currentTarget.dataset;
                // TODO: change modals to non-bootstrap
                $(lightBox).modal("show");
                ReactDOM.render(
                    <LightBox
                        albumId={parseInt(album, 10)}
                        page={parseInt(page, 10)}
                        selectedPhotoId={parseInt(photoId, 10)}
                    />,
                    targetNode
                );
            });
        }
    }

    static initControls() {
        const controls = {};
        const getControlClass = (action) => {
            switch (action) {
                case "rotate-left":
                case "rotate-right":
                    return RotateControl;
                default:
                    return Control;
            }
        };

        $(".controls").on("click", "[data-action]", function (event) {
            event.preventDefault();
            const node = this;

            let control,
                action = node.dataset.action,
                $figure = $(this).closest("figure");

            if (action === "set-cover") {
                const photoNode = node
                    .closest("article")
                    .querySelector(".album-photo");
                return setCover(photoNode);
            }

            let cls = getControlClass(action);
            control = controls[action] || new cls($(this), $figure);

            control.toggle();
            return false;
        });
    }

    static initPhotoEdit() {
        $('body.photo-update input[name="album"]').change(function () {
            // if checked, uncheck other albums
            if ($(this).is(":checked")) {
                $('input[name="album"]').not(this).prop("checked", false);
            }
        });

        // scrolling through the carousel
        $("body.photo-update #carousel-album").on(
            "mousewheel",
            function (event) {
                event.preventDefault();

                if (event.originalEvent.wheelDelta / 120 > 0) {
                    $(this).carousel("next");
                } else {
                    $(this).carousel("prev");
                }

                return false;
            }
        );
    }
}

$('.controls [data-toggle="popover"]').popover();

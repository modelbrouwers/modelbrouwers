import "jquery";
import Handlebars from "../general/hbs-pony";
import { PhotoConsumer } from "../data/albums/photo";
import { RotateControl, Control } from "./photo-detail";
import { PhotoUpload } from "./upload";

export default class Page {
    static init() {
        this.photoConsumer = new PhotoConsumer();

        this.initLightbox();
        this.initControls();
        new PhotoUpload();
        this.initPhotoEdit();
    }

    static initLightbox() {
        const lightBox = document.getElementById("modal-lightbox");
        const $lightbox = $(lightBox);
        const $lightboxBody = $lightbox.find(".modal-content");
        const photoThumbs = $("#photo-thumbs");

        const renderLightbox = (currentID, photos) => {
            const current = photos.find(e => e.id === currentID);
            current.state = { selected: true };
            const context = {
                photos: photos,
                current: current
            };
            Handlebars.render("albums::photo-lightbox", context)
                .then(html => {
                    $lightboxBody.append(html);
                    $lightbox.find(".active img").on("load", function() {
                        $("#image-loader").hide();
                    });
                })
                .catch(console.error);
        };

        /* Closure to render the current photo in the lightbox */
        const getLightboxRenderer = id => {
            const currentID = id;
            return photos => {
                renderLightbox(currentID, photos);
                $lightbox.find(".carousel").trigger("slide.bs.carousel");
            };
        };

        photoThumbs.on("click", ".album-photo", event => {
            event.preventDefault();

            const id = $(event.target)
                .closest(".album-photo")
                .data("id");

            // remove all 'old' bits
            $lightboxBody.find(".modal-body").remove();
            $("#image-loader").show();

            // bring up the modal with spinner
            $lightbox.modal("show");

            // fetch the photo details from the Api
            const { album, page } = lightBox.dataset;
            this.photoConsumer
                .getForAlbum(album, page)
                .then(getLightboxRenderer(id))
                .catch(console.error);
        });
    }

    static initControls() {
        const controls = {};
        const getControlClass = action => {
            switch (action) {
                case "rotate-left":
                case "rotate-right":
                    return RotateControl;
                default:
                    return Control;
            }
        };

        $(".controls").on("click", "[data-action]", function(event) {
            event.preventDefault();

            let control,
                action = $(this).data("action"),
                $figure = $(this).closest("figure");

            let cls = getControlClass(action);
            control = controls[action] || new cls($(this), $figure);
            control.toggle();
            return false;
        });
    }

    static initPhotoEdit() {
        $('body.photo-update input[name="album"]').change(function() {
            // if checked, uncheck other albums
            if ($(this).is(":checked")) {
                $('input[name="album"]')
                    .not(this)
                    .prop("checked", false);
            }
        });

        // scrolling through the carousel
        $("body.photo-update #carousel-album").on("mousewheel", function(
            event
        ) {
            event.preventDefault();

            if (event.originalEvent.wheelDelta / 120 > 0) {
                $(this).carousel("next");
            } else {
                $(this).carousel("prev");
            }

            return false;
        });
    }
}

$('.controls [data-toggle="popover"]').popover();

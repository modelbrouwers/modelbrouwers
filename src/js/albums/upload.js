import "jquery";
import qq from "fine-uploader";

export class PhotoUpload {
    constructor() {
        const albumChooser = $("#carousel-album");
        let album, uploader;
        const elem = document.getElementById("uploader");

        if (elem) {
            uploader = new qq.FineUploader({
                element: elem,
                request: {
                    endpoint: endpoint,
                    inputName: "image",
                    filenameParam: "description",
                    customHeaders: {
                        Accept: "text/plain", // otherwise DRF complains
                        "X-CSRFToken": window.csrf_token
                    }
                },
                retry: {
                    enableAuto: false
                },
                validation: {
                    allowedExtensions: ["jpeg", "jpg", "gif", "png"] // only images
                },
                autoUpload: autoUpload,
                callbacks: {
                    onComplete: function(event, succeeded, failed) {
                        if (failed.length === 0) {
                            window.location = decodeURI(
                                window.albumDetail
                            ).format(album);
                        }
                    },
                    onSubmit: function() {
                        const ok = setAlbum();
                        if (ok) {
                            const $dest = $("#upload-form");
                            $("html, body").animate(
                                {
                                    scrollTop: $dest.offset().top
                                },
                                500
                            );
                        }
                        return ok;
                    }
                }
            });
        }

        var setAlbum = function() {
            var checked = $('#upload-form input[name="album"]:checked');
            if (checked.length !== 1) {
                $("#modal-albums").modal("show");
                return false;
            }

            album = parseInt(checked.val(), 10);
            var params = { album: album };
            if (!qq.supportedFeatures.uploadCustomHeaders) {
                params.csrfmiddlewaretoken = window.csrf_token;
            }
            uploader.setParams(params);
            return true;
        };

        $(".cancel").click(function(e) {
            uploader.cancel(id);
        });

        $("#trigger-upload").click(function(e) {
            e.preventDefault();
            // TODO: multi upload
            setAlbum();
            uploader.uploadStoredFiles();
            return false;
        });

        var focusActiveAlbum = function() {
            var checked = albumChooser.find("input:checked").next();
            var hasChecked = checked.length == 1;

            var slideNext = function() {
                if (hasChecked && !checked.is(":visible")) {
                    albumChooser.carousel("next");
                    setTimeout(slideNext, 100);
                }
            };
            slideNext();
        };
        focusActiveAlbum();

        // Use the FineUploader flags to hide/show relevant DOM elements.
        var featureDetection = function() {
            if (!qq.supportedFeatures.fileDrop) {
                $('[data-feature="fileDrop"]').toggleClass("hidden");
            }
        };
        featureDetection();

        // scrolling through the carousel
        $("#carousel-album").on("mousewheel", function(event) {
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

import React from "react";
import ReactDOM from "react-dom";
import { IntlProvider } from "react-intl";

import { getIntlProviderProps } from "../i18n";

import "jquery";
import "bootstrap";

import { AlbumConsumer } from "../data/albums/album";
import { PhotoConsumer } from "../data/albums/photo";

import Formset from "../ponyjs/forms/formsets.js";

import Handlebars from "../general/hbs-pony";

import AlbumPicker from "./AlbumPicker";

let conf = {
    input_url: '.formset-form input[type="url"]',
    formset: ".formset-form",
    photo_picker: {
        picker: "#photo-picker",
        add_url: "#add-url-photo",
        body: "#carousel-album .carousel-inner",
        list: "#photo-picker .photo-list",
    },
};

class PhotoFormset extends Formset {
    get template() {
        if (!this._template) {
            this._template = $("#empty-form").html();
        }
        return this._template;
    }
}

let photoFormset = new PhotoFormset("photos");

let showPhotos = function (event) {
    // always show the loader first
    $(conf.photo_picker.list).removeClass("hidden");
    Handlebars.render("general::loader", {}, $(conf.photo_picker.list));

    if (!$(this).is(":checked")) {
        $(conf.photo_picker.list).addClass("hidden");
        return;
    }

    // reset other checkboxes
    $(conf.photo_picker.body)
        .find('input[type="checkbox"]:checked')
        .not(this)
        .prop("checked", false);

    let albumId = parseInt($(this).val(), 10);

    const photoConsumer = new PhotoConsumer();
    photoConsumer
        .getAllForAlbum(albumId)
        .then((photos) => {
            console.log(photos);
            return Handlebars.render("builds::album-photo-picker", { photos });
        })
        .then((html) => {
            $(conf.photo_picker.list).html(html);
        })
        .catch(console.error);
};

let togglePhotoPicker = function (event) {
    event.preventDefault();
    $($(this).data("target")).toggleClass("hidden");
    return false;
};

let showPreview = function ($form, url) {
    let $preview = $form.find(".preview");
    $preview.addClass("hidden"); // always hide, only show when real urls work

    let img = new Image();
    img.onload = function () {
        $form.find("img").attr("src", url);
        $preview.removeClass("hidden");
    };
    img.src = url; // trigger loading
};

let previewUrl = function (event) {
    let url = $(this).val();
    let $form = $(this).closest(".formset-form");
    let $img = $form.find("img");
    showPreview($form, url);
};

let photoFormMapping = {};

let addRemoveAlbumPhoto = function (event) {
    let photoId = $(this).data("id");
    let add = $(this).is(":checked");

    if (add) {
        let [html, index] = photoFormset.addForm();
        $(conf.formset).closest("fieldset").append(html);
        let $form = $(conf.formset).last();
        photoFormMapping[photoId] = $form;
        $form.find(".url").hide();
        photoFormset.setData(index, { photo: photoId });
        let url = $(this).siblings("label").find("img").data("large");
        $form.find('[data-toggle="popover"]').popover();
        showPreview($form, url);
    } else {
        let $form = photoFormMapping[photoId];
        $form.remove();
    }
};

let addUrlForm = function (event) {
    event.preventDefault();
    let [html, index] = photoFormset.addForm();
    $(conf.formset).closest("fieldset").append(html);
    let $form = $(conf.formset).last();
    $form.find(".album").hide();
    $(window, "body").scrollTop($form.position().top);
    $form.find("input:visible").focus();
    $form.find('[data-toggle="popover"]').popover();
    return false;
};

// either show album or url, depending on which one is entered
let showAlbumOrUrls = function () {
    $(conf.formset).each((i, form) => {
        let $form = $(form);
        let prefix = `id_photos-${i}`;
        let photo = $(form).find(`#${prefix}-photo`).val();
        if (photo) {
            $form.find(".url").hide();
        } else {
            $form.find(".album").hide();
        }
    });
};

let selectedAlbumId = null;

const renderAlbumPicker = (node, intlProviderProps) => {
    const onAlbumSelected = (albumId) => {
        selectedAlbumId = parseInt(albumId, 10);
        renderAlbumPicker(node, intlProviderProps);
    };

    ReactDOM.render(
        <IntlProvider {...intlProviderProps}>
            <AlbumPicker
                onSelect={onAlbumSelected}
                selectedAlbumId={selectedAlbumId}
            />
        </IntlProvider>,
        node
    );
};

const initBuildForm = async () => {
    // only initialize if there is a postable form
    const form = document.querySelector('form[method="post"]');
    if (!form) return;

    // bind change handler + trigger to display url previews
    $("fieldset").on("change, keyup", conf.input_url, previewUrl);
    $(`fieldset ${conf.input_url}`).change();

    // bind photo picker events
    $(conf.photo_picker.body).on(
        "change",
        'input[type="checkbox"]',
        showPhotos
    );
    $(conf.photo_picker.list).on(
        "change",
        'input[type="checkbox"]',
        addRemoveAlbumPhoto
    );
    $(`[data-target="${conf.photo_picker.picker}"]`).on(
        "click",
        togglePhotoPicker
    );

    // bind trigger to add a url form
    $(conf.photo_picker.add_url).on("click", addUrlForm);

    // properly display the formset forms, if any
    showAlbumOrUrls();

    // rendering album picker with React
    const intlProviderProps = await getIntlProviderProps();
    const albumPicker = document.querySelector(".react-album-picker");
    renderAlbumPicker(albumPicker, intlProviderProps);
};

export default initBuildForm;

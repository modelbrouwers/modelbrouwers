import React from "react";
import ReactDOM from "react-dom";
import { IntlProvider } from "react-intl";

import { getIntlProviderProps } from "../i18n";

import "jquery";
import "bootstrap";

import Formset from "../ponyjs/forms/formsets.js";

import AlbumPicker from "./AlbumPicker";
import PhotoPicker from "./PhotoPicker";
import Image from "./Image";

let conf = {
    input_url: '.formset-form input[type="url"]',
    formset: ".formset-form",
    photo_picker: {
        add_url: "#add-url-photo",
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

// refactored - above this is old code

/**
 * Synchronize the formset when a photo is selected.
 */
const onPhotoSelected = (photo) => {
    // TODO: refactor all these formset shenanigans to React too
    const formsetContainer = document.querySelector(".formset-container");
    const [html, index] = photoFormset.addForm();
    formsetContainer.insertAdjacentHTML("beforeend", html);
    const formNode = formsetContainer.lastElementChild;
    photoFormMapping[photo.id] = formNode;
    formNode.querySelector(".url").style.display = "none";
    photoFormset.setData(index, { photo: photo.id });
    const url = photo.image.large;
    const previewNode = formNode.querySelector(".preview");
    ReactDOM.render(
        <Image src={photo.image.large} alt={photo.description} />,
        previewNode.querySelector(".thumbnail")
    );
    previewNode.classList.remove("hidden");
    // TODO: de-jQuery-ify
    const popoverNode = formNode.querySelector('[data-toggle="popover"]');
    $(popoverNode).popover();
};

/**
 * Synchronize the formset when a photo is de-selected.
 */
const onPhotoDeselected = (photo) => {
    const formNode = photoFormMapping[photo.id];
    formNode.parentNode.removeChild(formNode);
};

let selectedAlbumId = null;
let selectedPhotos = []; // TODO: populate this for edit forms

const renderAlbumPicker = (node, intlProviderProps) => {
    const onAlbumSelected = (albumId) => {
        selectedAlbumId = parseInt(albumId, 10);
        renderAlbumPicker(node, intlProviderProps);
        renderPhotoPicker(null, intlProviderProps);
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

const renderPhotoPicker = (node = null, intlProviderProps) => {
    if (node == null) {
        node = document.querySelector(".react-photo-picker");
    }

    const onPhotoToggle = (photo, checked) => {
        if (checked) {
            selectedPhotos.push(photo);
            onPhotoSelected(photo);
        } else {
            const index = selectedPhotos.indexOf(photo);
            selectedPhotos.splice(index, 1);
            onPhotoDeselected(photo);
        }
        renderPhotoPicker(node, intlProviderProps);
    };

    ReactDOM.render(
        <IntlProvider {...intlProviderProps}>
            <PhotoPicker
                albumId={selectedAlbumId}
                selectedPhotoIds={selectedPhotos.map((photo) => photo.id)}
                onToggle={onPhotoToggle}
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
    const photoPickerButton = document.querySelector(
        '[data-target="#photo-picker"]'
    );
    const photoPicker = document.getElementById("photo-picker");
    photoPickerButton.addEventListener("click", (event) => {
        event.preventDefault();
        photoPicker.classList.toggle("hidden");
    });

    // bind trigger to add a url form
    document
        .getElementById("add-url-photo")
        .addEventListener("click", (event) => {
            // event.preventDefault();
            addUrlForm(event);
        });

    // properly display the formset forms, if any
    showAlbumOrUrls();

    // rendering album picker with React
    const intlProviderProps = await getIntlProviderProps();
    const albumPicker = document.querySelector(".react-album-picker");
    renderAlbumPicker(albumPicker, intlProviderProps);
};

export default initBuildForm;

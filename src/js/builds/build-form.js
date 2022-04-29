import React from "react";
import ReactDOM from "react-dom";
import { IntlProvider } from "react-intl";

import Formset from "../ponyjs/forms/formsets.js";

import { getIntlProviderProps } from "../i18n";
import AlbumPicker from "./AlbumPicker";
import PhotoPicker from "./PhotoPicker";
import Image from "./Image";

class PhotoFormset extends Formset {
    get template() {
        if (!this._template) {
            this._template = $("#empty-form").html();
        }
        return this._template;
    }
}

let photoFormset = new PhotoFormset("photos");
let formsetContainer;
let photoFormMapping = {};
let selectedAlbumId = null;
let selectedPhotos = []; // TODO: populate this for edit forms

const addUrlForm = (event) => {
    event.preventDefault();
    const [html, index] = photoFormset.addForm();
    formsetContainer.insertAdjacentHTML("beforeend", html);
    const formNode = formsetContainer.lastElementChild;
    formNode.querySelector(".album").style.display = "none";
    formNode.scrollIntoView(true);
    formNode.querySelector("input[type='url']").focus();

    // TODO: de-jQuery-ify
    const popoverNode = formNode.querySelector('[data-toggle="popover"]');
    $(popoverNode).popover();
};

// either show album or url, depending on which one is entered
let showAlbumOrUrls = () => {
    const forms = document.querySelectorAll(
        ".formset-container > .formset-form"
    );
    forms.forEach((formNode, index) => {
        const photoId = formNode.querySelector(
            `#id_photos-${index}-photo`
        ).value;
        if (photoId) {
            formNode.querySelector(".url").style.display = "none";
            // TODO: fetch and add to selectedPhotos
        } else {
            formNode.querySelector(".album").style.display = "none";
        }
    });
};

/**
 * Synchronize the formset when a photo is selected.
 */
const onPhotoSelected = (photo) => {
    // TODO: refactor all these formset shenanigans to React too
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

const onURLFieldChanged = ({ target }) => {
    if (target.tagName !== "INPUT") return;
    if (target.type !== "url") return;
    const formNode = target.closest(".formset-form");
    const previewNode = formNode.querySelector(".preview");
    ReactDOM.render(
        <Image src={target.value} alt={`URL: ${target.value}`} />,
        previewNode.querySelector(".thumbnail")
    );
    previewNode.classList.remove("hidden");
};

const initBuildForm = async () => {
    // only initialize if there is a postable form
    const form = document.querySelector('form[method="post"]');
    if (!form) return;

    formsetContainer = document.querySelector(".formset-container");

    // bind change handler + trigger to display url previews
    formsetContainer.addEventListener("change", onURLFieldChanged, false);
    formsetContainer.addEventListener("keyup", onURLFieldChanged, false);
    // fire on change event manually on load
    const changeEvent = new Event("change");
    const urlInputs = formsetContainer.querySelectorAll(
        ".formset-form input[type='url']"
    );
    for (const input of urlInputs) {
        input.dispatchEvent(changeEvent);
    }

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
        .addEventListener("click", addUrlForm);

    // properly display the formset forms, if any
    showAlbumOrUrls();

    // rendering album picker with React
    const intlProviderProps = await getIntlProviderProps();
    const albumPicker = document.querySelector(".react-album-picker");
    renderAlbumPicker(albumPicker, intlProviderProps);
};

export default initBuildForm;

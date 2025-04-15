import React from 'react';
import {createRoot} from 'react-dom/client';
import {IntlProvider} from 'react-intl';

import {getIntlProviderProps} from '../i18n';
import Formset from '../ponyjs/forms/formsets.js';
import AlbumPicker from './AlbumPicker';
import Image from './Image';
import PhotoPicker from './PhotoPicker';

class PhotoFormset extends Formset {
  get template() {
    if (!this._template) {
      this._template = $('#empty-form').html();
    }
    return this._template;
  }
}

let photoFormset = new PhotoFormset('photos');
let formsetContainer;
let photoFormMapping = {};
let selectedAlbumId = null;
let selectedPhotoIds = []; // TODO: populate this for edit forms

let albumPickerRoot = null;
let photoPickerRoot = null;

const addUrlForm = event => {
  event.preventDefault();
  const [html, index] = photoFormset.addForm();
  formsetContainer.insertAdjacentHTML('beforeend', html);
  const formNode = formsetContainer.lastElementChild;
  formNode.querySelector('.album').style.display = 'none';
  formNode.scrollIntoView(true);
  formNode.querySelector("input[type='url']").focus();

  // TODO: de-jQuery-ify
  const popoverNode = formNode.querySelector('[data-toggle="popover"]');
  $(popoverNode).popover();
};

// either show album or url, depending on which one is entered
let showAlbumOrUrls = () => {
  const forms = document.querySelectorAll('.formset-container > .formset-form');
  forms.forEach((formNode, index) => {
    const photoId = formNode.querySelector(`#id_photos-${index}-photo`).value;
    if (photoId) {
      formNode.querySelector('.url').style.display = 'none';
      selectedPhotoIds.push(parseInt(photoId, 10));
    } else {
      formNode.querySelector('.album').style.display = 'none';
    }
  });
};

/**
 * Synchronize the formset when a photo is selected.
 */
const onPhotoSelected = photo => {
  // TODO: refactor all these formset shenanigans to React too
  const [html, index] = photoFormset.addForm();
  formsetContainer.insertAdjacentHTML('beforeend', html);
  const formNode = formsetContainer.lastElementChild;
  photoFormMapping[photo.id] = formNode;
  formNode.querySelector('.url').style.display = 'none';
  photoFormset.setData(index, {photo: photo.id});
  const url = photo.image.large;
  const previewNode = formNode.querySelector('.preview');
  const root = previewNode.querySelector('.thumbnail');
  root.render(<Image src={photo.image.large} alt={photo.description} />);
  previewNode.classList.remove('hidden');
  // TODO: de-jQuery-ify
  const popoverNode = formNode.querySelector('[data-toggle="popover"]');
  $(popoverNode).popover();
};

/**
 * Synchronize the formset when a photo is de-selected.
 */
const onPhotoDeselected = photo => {
  const formNode = photoFormMapping[photo.id];
  formNode.parentNode.removeChild(formNode);
};

const renderAlbumPicker = (root, intlProviderProps) => {
  const onAlbumSelected = albumId => {
    selectedAlbumId = parseInt(albumId, 10);
    renderAlbumPicker(root, intlProviderProps);
    renderPhotoPicker(null, intlProviderProps);
  };

  root.render(
    <IntlProvider {...intlProviderProps}>
      <AlbumPicker onSelect={onAlbumSelected} selectedAlbumId={selectedAlbumId} />
    </IntlProvider>,
  );
};

const renderPhotoPicker = (root = photoPickerRoot, intlProviderProps) => {
  if (root == null) {
    photoPickerRoot = createRoot(document.querySelector('.react-photo-picker'));
    root = photoPickerRoot;
  }

  const onPhotoToggle = (photo, checked) => {
    if (checked) {
      selectedPhotoIds.push(photo.id);
      onPhotoSelected(photo);
    } else {
      const index = selectedPhotoIds.indexOf(photo.id);
      selectedPhotoIds.splice(index, 1);
      onPhotoDeselected(photo);
    }
    renderPhotoPicker(root, intlProviderProps);
  };

  root.render(
    <IntlProvider {...intlProviderProps}>
      <PhotoPicker
        albumId={selectedAlbumId}
        selectedPhotoIds={selectedPhotoIds}
        onToggle={onPhotoToggle}
      />
    </IntlProvider>,
  );
};

const onURLFieldChanged = ({target}) => {
  if (target.tagName !== 'INPUT') return;
  if (target.type !== 'url') return;
  const formNode = target.closest('.formset-form');
  const previewNode = formNode.querySelector('.preview');

  const root = previewNode.querySelector('.thumbnail');
  root.render(<Image src={target.value} alt={`URL: ${target.value}`} />);
  previewNode.classList.remove('hidden');
};

const initBuildForm = async () => {
  // only initialize if there is a postable form
  const form = document.querySelector('form[method="post"]');
  if (!form) return;

  formsetContainer = document.querySelector('.formset-container');

  // bind change handler + trigger to display url previews
  formsetContainer.addEventListener('change', onURLFieldChanged, false);
  formsetContainer.addEventListener('keyup', onURLFieldChanged, false);
  // fire on change event manually on load
  const changeEvent = new Event('change');
  const urlInputs = formsetContainer.querySelectorAll(".formset-form input[type='url']");
  for (const input of urlInputs) {
    input.dispatchEvent(changeEvent);
  }

  // bind photo picker events
  const photoPickerButton = document.querySelector('[data-target="#photo-picker"]');
  const photoPicker = document.getElementById('photo-picker');
  photoPickerButton.addEventListener('click', event => {
    event.preventDefault();
    photoPicker.classList.toggle('hidden');
  });

  // bind trigger to add a url form
  document.getElementById('add-url-photo').addEventListener('click', addUrlForm);

  // properly display the formset forms, if any
  showAlbumOrUrls();

  // rendering album picker with React
  const intlProviderProps = await getIntlProviderProps();
  const albumPicker = document.querySelector('.react-album-picker');
  albumPickerRoot = createRoot(albumPicker);
  renderAlbumPicker(albumPickerRoot, intlProviderProps);
};

export default initBuildForm;

import $ from 'jquery';
import React from 'react';
import {createRoot} from 'react-dom/client';

import {setAsCover} from '@/data/albums/photo';

import LightBox from './LightBox';
import {Control, RotateControl} from './photo-detail';
import {PhotoUpload} from './upload';

const setCover = async photoNode => {
  const photoId = parseInt(photoNode.dataset.id);
  await setAsCover(photoId);
  $('.cover').removeClass('cover');
  photoNode.classList.add('cover');
};

export default class Page {
  static init() {
    this.initLightbox();
    this.initControls();
    new PhotoUpload();
    this.initPhotoEdit();
  }

  static initLightbox() {
    const lightBox = document.getElementById('modal-lightbox');
    if (!lightBox) return;
    const targetNode = lightBox.querySelector('.modal-content');

    const thumbs = document.querySelectorAll('#photo-thumbs .album-photo');
    if (!thumbs.length) return;

    const {album, page} = lightBox.dataset;

    for (const thumb of thumbs) {
      thumb.addEventListener('click', event => {
        event.preventDefault();
        const {id: photoId} = event.currentTarget.dataset;
        // TODO: change modals to non-bootstrap
        $(lightBox).modal('show');
        const root = createRoot(targetNode);
        root.render(
          <LightBox
            albumId={parseInt(album, 10)}
            page={parseInt(page, 10)}
            selectedPhotoId={parseInt(photoId, 10)}
          />,
        );
      });
    }
  }

  static initControls() {
    const controls = {};
    const getControlClass = action => {
      switch (action) {
        case 'rotate-left':
        case 'rotate-right':
          return RotateControl;
        default:
          return Control;
      }
    };

    $('.controls').on('click', '[data-action]', function (event) {
      event.preventDefault();
      const node = this;

      let control,
        action = node.dataset.action,
        $figure = $(this).closest('figure');

      if (action === 'set-cover') {
        const photoNode = node.closest('article').querySelector('.album-photo');
        setCover(photoNode);
        return;
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
      if ($(this).is(':checked')) {
        $('input[name="album"]').not(this).prop('checked', false);
      }
    });

    // scrolling through the carousel
    $('body.photo-update #carousel-album').on('mousewheel', function (event) {
      event.preventDefault();

      if (event.originalEvent.wheelDelta / 120 > 0) {
        $(this).carousel('next');
      } else {
        $(this).carousel('prev');
      }

      return false;
    });
  }
}

$('.controls [data-toggle="popover"]').popover();

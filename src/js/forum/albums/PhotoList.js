import PropTypes from 'prop-types';
import React from 'react';
import {FormattedMessage, useIntl} from 'react-intl';

import {Photo} from '../../data/albums/photo';

const PhotoPreview = ({thumbnailUrl, description = '', onSelect}) => {
  const intl = useIntl();
  return (
    <figure className="album-photo">
      <a
        href="#"
        onClick={onSelect}
        aria-label={intl.formatMessage({
          description: 'Accessible label for photo insert link',
          defaultMessage: 'Insert photo',
        })}
      >
        <img src={thumbnailUrl} alt={description} />
      </a>
      <figcaption>{description}</figcaption>
    </figure>
  );
};

PhotoPreview.propTypes = {
  thumbnailUrl: PropTypes.string.isRequired,
  description: PropTypes.string,
  onSelect: PropTypes.func.isRequired,
};

const PhotoList = ({photos = null, onPhotoSelect}) => {
  if (photos && photos.length === 0) {
    return (
      <ul id="photo-list">
        <li>
          <FormattedMessage
            id="forum.albums.sidebar.noPhotosYet"
            defaultMessage="There are no photo's in this album yet. You can upload some <link>here</link>."
            values={{
              link: chunks => (
                <a href="/albums/upload/" target="_blank">
                  {chunks}
                </a>
              ),
            }}
          />
        </li>
      </ul>
    );
  }
  return (
    <ul id="photo-list">
      {photos.map(photo => (
        <li key={photo.id}>
          <PhotoPreview
            thumbnailUrl={photo.image.thumb}
            description={photo.description}
            onSelect={onPhotoSelect.bind(this, photo)}
          />
        </li>
      ))}
    </ul>
  );
};

PhotoList.propTypes = {
  photos: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      description: PropTypes.string.isRequired,
      image: PropTypes.shape({
        thumb: PropTypes.string.isRequired,
        large: PropTypes.string.isRequired,
      }).isRequired,
      user: PropTypes.number.isRequired,
    }),
  ),
  onPhotoSelect: PropTypes.func.isRequired,
};

export default PhotoList;

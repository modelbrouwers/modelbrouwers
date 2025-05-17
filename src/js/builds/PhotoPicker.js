import PropTypes from 'prop-types';
import React from 'react';
import useAsync from 'react-use/esm/useAsync';

import Loader from 'components/Loader';

import {listAllAlbumPhotos} from '@/data/albums/photo';

import Image from './Image';

const PhotoInput = ({id, image, description, selected, onChange}) => {
  const htmlId = `id_build-photo-${id}`;

  const onCheckboxChange = () => {
    onChange(id, !selected);
  };

  return (
    <div className="photo-picker__input">
      <input
        type="checkbox"
        name={`build-photo-${id}`}
        id={htmlId}
        className="photo-picker__checkbox"
        onChange={onCheckboxChange}
        checked={selected}
      />
      <label htmlFor={htmlId}>
        <figure className="thumbnail album-photo">
          <Image src={image.thumb} alt={description} />
        </figure>
      </label>
      <i className="fa fa-check fa-3x"></i>
    </div>
  );
};

PhotoInput.propTypes = {
  id: PropTypes.number.isRequired,
  image: PropTypes.shape({
    thumb: PropTypes.string.isRequired,
    large: PropTypes.string.isRequired,
  }).isRequired,
  description: PropTypes.string.isRequired,
};

const PhotoPicker = ({albumId, selectedPhotoIds = [], onToggle}) => {
  const {
    loading,
    error,
    value: photos,
  } = useAsync(async () => await listAllAlbumPhotos(albumId), [albumId]);

  if (loading) {
    return <Loader center />;
  }

  if (error) {
    console.error(error);
    return 'Something went wrong.';
  }

  const onChange = (id, checked) => {
    const photo = photos.find(photo => photo.id === id);
    onToggle(photo, checked);
  };

  return (
    <div className="photo-picker">
      {photos.map(photo => (
        <PhotoInput
          key={photo.id}
          {...photo}
          selected={selectedPhotoIds.includes(photo.id)}
          onChange={onChange}
        />
      ))}
    </div>
  );
};

PhotoPicker.propTypes = {
  albumId: PropTypes.number.isRequired,
  selectedPhotoIds: PropTypes.arrayOf(PropTypes.number.isRequired),
  onToggle: PropTypes.func.isRequired,
};

export default PhotoPicker;

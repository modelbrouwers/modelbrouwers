import useAsync from 'react-use/esm/useAsync';

import Loader from 'components/Loader';

import {PhotoData, listAllAlbumPhotos} from '@/data/albums/photo';

import Image from './Image';

interface PhotoInputProps {
  id: number;
  image: {
    thumb: string;
    large: string;
  };
  description: string;
  selected: boolean;
  onChange: (id: number, selected: boolean) => void;
}

const PhotoInput: React.FC<PhotoInputProps> = ({id, image, description, selected, onChange}) => {
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

export interface PhotoPickerProps {
  albumId: number;
  selectedPhotoIds: number[];
  onToggle: (photo: PhotoData, checked: boolean) => void;
}

const PhotoPicker: React.FC<PhotoPickerProps> = ({albumId, selectedPhotoIds = [], onToggle}) => {
  const {
    loading,
    error,
    value: photos = [],
  } = useAsync(async () => await listAllAlbumPhotos(albumId), [albumId]);

  if (loading) {
    return <Loader center />;
  }

  if (error) {
    console.error(error);
    return 'Something went wrong.';
  }

  const onChange = (id: number, checked: boolean) => {
    const photo = photos.find(photo => photo.id === id)!;
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

export default PhotoPicker;

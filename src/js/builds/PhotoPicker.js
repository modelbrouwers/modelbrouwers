import React from "react";
import PropTypes from "prop-types";
import useAsync from "react-use/esm/useAsync";

import { STATIC } from "../constants";
import Loader from "../components/loaders";
import { PhotoConsumer } from "../data/albums/photo";

const THUMB = `${STATIC}/images/thumb.png`;

const photoConsumer = new PhotoConsumer();

const PhotoInput = ({ id, image, description, selected, onChange }) => {
    const htmlId = `id_build-photo-${id}`;
    return (
        <div className="photo-picker__input">
            <input
                type="checkbox"
                onChange={onChange}
                name={`build-photo-${id}`}
                id={htmlId}
                className="photo-picker__checkbox"
            />
            <label htmlFor={htmlId}>
                <figure className="thumbnail album-photo">
                    <img
                        src={image.thumb}
                        alt={description}
                        onError={(event) => {
                            event.target.onerror = null;
                            event.target.src = THUMB;
                        }}
                    />
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

const PhotoPicker = ({ albumId, selectedPhotoIds = [], onSelect }) => {
    const {
        loading,
        error,
        value: photos,
    } = useAsync(
        async () => await photoConsumer.getAllForAlbum(albumId),
        [albumId]
    );

    if (loading) {
        return <Loader center />;
    }

    if (error) {
        console.error(error);
        return "Something went wrong.";
    }

    const onPhotoSelected = (event) => {
        console.log(event.target);
        const { value: photoId } = event.target;
        const photo = photos.find(
            (photo) => photo.id === parseInt(photoId, 10)
        );
        onSelect(photo);
    };

    return (
        <div className="photo-picker">
            {photos.map((photo) => (
                <PhotoInput
                    key={photo.id}
                    {...photo}
                    selected={selectedPhotoIds.includes(photo.id)}
                    onChange={onPhotoSelected}
                />
            ))}
        </div>
    );
};

PhotoPicker.propTypes = {
    albumId: PropTypes.number.isRequired,
    selectedPhotoIds: PropTypes.arrayOf(PropTypes.number.isRequired),
    onSelect: PropTypes.func.isRequired,
};

export default PhotoPicker;

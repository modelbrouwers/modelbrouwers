import React from "react";
import PropTypes from "prop-types";
import useAsync from "react-use/esm/useAsync";

import { Navigation, Scrollbar, A11y } from "swiper";
import { Swiper, SwiperSlide } from "swiper/react";

import { Photo, PhotoConsumer } from "../data/albums/photo";

const photoConsumer = new PhotoConsumer();

const LightBox = ({ albumId, page, selectedPhotoId }) => {
    const {
        loading,
        error,
        value: photos = [],
    } = useAsync(async () => {
        return await photoConsumer.getForAlbum(albumId, page);
    }, [albumId, page]);

    if (loading) {
        return (
            <div className="text-center" id="image-loader">
                <i className="fa fa-pulse fa-spinner fa-4x"></i>
            </div>
        );
    }

    const selectedPhoto = photos.find((photo) => photo.id === selectedPhotoId);
    const selectedPhotoIndex = photos.indexOf(selectedPhoto);

    return (
        <div className="modal-body" style={{ height: "100%" }}>
            <Swiper
                modules={[Navigation, Scrollbar, A11y]}
                initialSlide={selectedPhotoIndex}
                navigation
                scrollbar={{ draggable: true }}
            >
                {photos.map((photo) => (
                    <SwiperSlide key={photo.id}>
                        <div className="image-wrapper">
                            <img
                                src={photo.image.large}
                                className="img-responsive"
                                alt={photo.description}
                            />
                        </div>
                    </SwiperSlide>
                ))}
            </Swiper>
        </div>
    );
};

LightBox.propTypes = {
    albumId: PropTypes.number.isRequired,
    page: PropTypes.number.isRequired,
    selectedPhotoId: PropTypes.number.isRequired,
    photos: PropTypes.arrayOf(PropTypes.instanceOf(Photo)),
};

export default LightBox;

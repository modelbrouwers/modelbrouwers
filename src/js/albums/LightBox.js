import PropTypes from 'prop-types';
import React, {useEffect, useRef} from 'react';
import useAsync from 'react-use/esm/useAsync';
import {A11y, Navigation, Scrollbar} from 'swiper';
import {Swiper, SwiperSlide} from 'swiper/react';

import Loader from '@/components/Loader';
import {listAlbumPhotos} from '@/data/albums/photo';

const getPhotoIndex = (photos, photoId) => {
  const photo = photos.find(photo => photo.id === photoId);
  return photos.indexOf(photo);
};

const LightBox = ({albumId, page, selectedPhotoId}) => {
  const swiperRef = useRef(null);
  const {
    loading,
    error,
    value: photos = [],
  } = useAsync(async () => await listAlbumPhotos({album: albumId, page}), [albumId, page]);

  useEffect(() => {
    const swiper = swiperRef.current;
    if (!swiper) return;
    if (!photos.length) return;
    const expectedIndex = getPhotoIndex(photos, selectedPhotoId);
    if (swiper.activeIndex !== expectedIndex) {
      swiper.slideTo(expectedIndex);
    }
  }, [swiperRef, photos, selectedPhotoId]);

  if (loading) {
    return <Loader center />;
  }

  return (
    <div className="modal-body" style={{height: '100%'}}>
      <Swiper
        modules={[Navigation, Scrollbar, A11y]}
        initialSlide={getPhotoIndex(photos, selectedPhotoId)}
        navigation
        scrollbar={{draggable: true}}
        onSwiper={swiper => (swiperRef.current = swiper)}
      >
        {photos.map(photo => (
          <SwiperSlide key={photo.id}>
            <div className="image-wrapper">
              <img src={photo.image.large} className="img-responsive" alt={photo.description} />
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
};

export default LightBox;

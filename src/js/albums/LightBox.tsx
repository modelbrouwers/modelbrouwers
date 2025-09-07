import React, {useEffect, useRef, useState} from 'react';
import useAsync from 'react-use/esm/useAsync';
// @ts-expect-error
import {A11y, Navigation, Scrollbar} from 'swiper';
import {Swiper, SwiperSlide} from 'swiper/react';
import type {Swiper as SwiperCls} from 'swiper/types';

import Loader from '@/components/Loader';
import Modal from '@/components/modals/Modal';
import {type PhotoData, listAlbumPhotos} from '@/data/albums/photo';

const getPhotoIndex = (photos: PhotoData[], photoId: number): number => {
  const photo = photos.find(photo => photo.id === photoId);
  return photo ? photos.indexOf(photo) : -1;
};

export interface LightBoxProps {
  albumId: number;
  page: number;
  selectedPhotoId: number;
}

const LightBox: React.FC<LightBoxProps> = ({albumId, page, selectedPhotoId}) => {
  const [isOpen, setIsOpen] = useState(true);
  const swiperRef = useRef<SwiperCls | null>(null);
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

  if (error) throw error;

  return (
    <div className="lightbox">
      <Modal isOpen={isOpen} onRequestClose={() => setIsOpen(false)}>
        {loading ? (
          <Loader center />
        ) : (
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
        )}
      </Modal>
    </div>
  );
};

export default LightBox;

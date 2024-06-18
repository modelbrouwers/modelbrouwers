import React from "react";
import PropTypes from "prop-types";
import useAsync from "react-use/esm/useAsync";
import { Scrollbar, A11y } from "swiper";
import { Swiper, SwiperSlide } from "swiper/react";

import { STATIC } from "../constants";
import { AlbumConsumer } from "../data/albums/album";
import Loader from "components/Loader";

const albumConsumer = new AlbumConsumer();

const CoverImage = ({ cover, title = "" }) => {
  const alt = cover ? `album: ${title}` : "album";
  const imgSrc = cover ? cover.url : `${STATIC}/images/thumb.png`;
  return <img src={imgSrc} className="img-responsive" alt={alt} />;
};

CoverImage.propTypes = {
  cover: PropTypes.shape({
    url: PropTypes.string.isRequired,
  }),
  title: PropTypes.string,
};

const AlbumInput = ({ id, cover, title = "", onChange, selected = false }) => {
  const htmlId = `id_album_${id}`;
  return (
    <div className="album-picker__input">
      <input
        type="radio"
        name="album"
        value={id}
        id={htmlId}
        className="album-picker__radio"
        onChange={onChange}
        checked={selected}
      />
      <label htmlFor={htmlId} className="thumbnail text-center">
        <CoverImage cover={cover} title={title} />
        <span className="h4">{title}</span>
      </label>
      <i className="fa fa-check fa-3x"></i>
    </div>
  );
};

AlbumInput.propTypes = {
  id: PropTypes.number.isRequired,
  cover: PropTypes.shape({
    url: PropTypes.string.isRequired,
  }),
  onChange: PropTypes.func.isRequired,
  title: PropTypes.string,
  selected: PropTypes.bool,
};

/**
 * Component displaying the available albums in slider, allowing one album to be
 * selected.
 * @param  {Function} options.onSelect Callback to invoke when an album is selected.
 * @return {JSX}
 */
const AlbumPicker = ({ onSelect, selectedAlbumId = null }) => {
  const {
    loading,
    error,
    value: albums,
  } = useAsync(async () => await albumConsumer.list(), []);

  if (loading) {
    return <Loader center />;
  }

  if (error) {
    console.error(error);
    return "Something went wrong.";
  }

  return (
    <div className="album-picker">
      <Swiper
        modules={[Scrollbar, A11y]}
        scrollbar={{ draggable: true }}
        height={155}
        slidesPerView={3}
        slidesPerGroup={3}
        breakpoints={{
          768: {
            slidesPerView: 5,
            slidesPerGroup: 4,
          },
        }}
      >
        {albums.map((album) => (
          <SwiperSlide key={album.id}>
            <AlbumInput
              {...album}
              selected={album.id === selectedAlbumId}
              onChange={(event) => onSelect(event.target.value)}
            />
          </SwiperSlide>
        ))}
      </Swiper>
    </div>
  );
};

AlbumPicker.propTypes = {
  onSelect: PropTypes.func.isRequired,
  selectedAlbumId: PropTypes.number,
};

export default AlbumPicker;

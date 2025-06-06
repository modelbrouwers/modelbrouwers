import PropTypes from 'prop-types';
import React from 'react';
import useAsync from 'react-use/esm/useAsync';

import {listOwnAlbums} from '@/data/albums/album';

const AlbumSelect = ({onChange, selected = null}) => {
  const {
    loading,
    error,
    value: albums,
  } = useAsync(async () => {
    const albums = await listOwnAlbums();
    if (albums.length && !selected) {
      onChange(albums[0]);
    }
    return albums;
  }, []);

  if (error) return error.message;

  return (
    <select
      name="album"
      value={selected ? selected.id.toString() : ''}
      onChange={event => {
        const album = albums.find(album => album.id.toString() === event.target.value);
        onChange(album);
      }}
    >
      {loading ? (
        <option value="">...</option>
      ) : (
        albums.map(album => (
          <option value={album.id.toString()} key={album.id}>
            {album.title}
          </option>
        ))
      )}
    </select>
  );
};

AlbumSelect.propTypes = {
  onChange: PropTypes.func.isRequired,
  selected: PropTypes.object,
};

export default AlbumSelect;

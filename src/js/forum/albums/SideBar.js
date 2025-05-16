import classNames from 'classnames';
import PerfectScrollbar from 'perfect-scrollbar';
import PropTypes from 'prop-types';
import React, {useEffect, useRef, useState} from 'react';
import {FormattedMessage} from 'react-intl';
import useAsync from 'react-use/esm/useAsync';

import Loader from '@/components/Loader';
import {getOwnPhoto, listOwnPhotos} from '@/data/albums/photo';

import AlbumSelect from './AlbumSelect';
import PhotoList from './PhotoList';
import PhotosPagination from './PhotosPagination';

const usePerfectScrollbar = () => {
  const containerRef = useRef(null);
  useEffect(() => {
    if (!containerRef.current) return;
    const container = containerRef.current;
    if (!container._psInstance) {
      container._psInstance = new PerfectScrollbar(container);
    }
    const ps = container._psInstance;
    return () => {
      if (ps) {
        ps.destroy();
        delete container._psInstance;
      }
    };
  });
  return containerRef;
};

const useLoadPhotos = (album, page = 1) => {
  const {
    loading,
    error,
    value: {photos = [], numPages = 0} = {},
  } = useAsync(async () => {
    if (!album) return [];
    const photosResponse = await listOwnPhotos({albumId: album.id, page});
    const numPages = Math.ceil(photosResponse.count / photosResponse.paginate_by);
    return {
      photos: photosResponse.results,
      numPages,
    };
  }, [album, page]);
  return {loading, error, photos, numPages};
};

const SideBar = ({onInsertPhoto}) => {
  const [closed, setClosed] = useState(true);
  const [album, setAlbum] = useState(null);
  const [page, setPage] = useState(1);

  const containerRef = usePerfectScrollbar();
  const {loading, error, photos, numPages} = useLoadPhotos(album, page);

  const className = classNames('box-sizing', {closed: closed, open: !closed});

  return (
    <>
      <div id="photo-sidebar" className={className} ref={containerRef}>
        <div className="pull-right">
          <div className="open-close" id="close-sidebar" onClick={() => setClosed(true)}>
            <i className="fa fa-times fa-2x" />
          </div>
        </div>

        <div>
          <section>
            <h2>
              <FormattedMessage id="forum.albums.sidebar.title" defaultMessage="Albums" />
            </h2>

            <AlbumSelect
              onChange={album => {
                setAlbum(album);
                setPage(1);
              }}
              selected={album}
            />
          </section>

          <section>
            <h2>
              <FormattedMessage id="forum.albums.sidebar.photos-title" defaultMessage="Photos" />
            </h2>
            <div id="photo-list-container">
              {loading ? <Loader center /> : null}

              <PhotoList
                photos={photos}
                onPhotoSelect={async ({id}, event) => {
                  event.preventDefault();
                  const photo = await getOwnPhoto(id);
                  const bbcode = `[photo data-id="${photo.id}"]${photo.image.large}[/photo]`;
                  onInsertPhoto(bbcode);
                }}
              />
            </div>

            <PhotosPagination page={page} numPages={numPages} onPageRequested={setPage} />
          </section>
        </div>
      </div>

      <div
        className="lid"
        onClick={() => setClosed(false)}
        role="button"
        aria-label="Toon albums en foto's"
      >
        <i className="fa fa-camera fa-rotate-270 fa-2x" />
      </div>
    </>
  );
};

SideBar.propTypes = {
  onInsertPhoto: PropTypes.func.isRequired,
};

export default SideBar;

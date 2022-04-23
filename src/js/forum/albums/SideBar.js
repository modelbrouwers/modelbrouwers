import React, { useState, useRef, useEffect } from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";
import classNames from "classnames";
import PerfectScrollbar from "perfect-scrollbar";
import useAsync from "react-use/esm/useAsync";

import Paginator from "../../scripts/paginator";
import AlbumSelect from "./AlbumSelect";
import PhotoList from "./PhotoList";

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

const useLoadPhotos = (album, page) => {
    const paginator = new Paginator();
    const {
        loading,
        error,
        value: photos = [],
    } = useAsync(async () => {
        const filters = page ? { page } : {};
        const photosResponse = await album.getPhotos(filters);
        paginator.paginate(photosResponse, page);
        return photosResponse.results;
    }, [album, page]);

    return {
        loading,
        error,
        photos,
        paginator,
    };
};

const SideBar = () => {
    const [closed, setClosed] = useState(true);
    const [album, setAlbum] = useState(null);
    const [page, setPage] = useState(null);

    const containerRef = usePerfectScrollbar();
    const { loading, error, photos, paginator } = useLoadPhotos(album, page);

    const className = classNames("box-sizing", {
        closed: closed,
        open: !closed,
    });

    return (
        <>
            <div id="photo-sidebar" className={className} ref={containerRef}>
                <div className="pull-right">
                    <div
                        className="open-close"
                        id="close-sidebar"
                        onClick={() => setClosed(true)}
                    >
                        <i className="fa fa-times fa-2x" />
                    </div>
                </div>

                <div>
                    <section>
                        <h2>
                            <FormattedMessage
                                id="forum.albums.sidebar.title"
                                defaultMessage="Albums"
                            />
                        </h2>

                        <AlbumSelect onChange={setAlbum} selected={album} />
                    </section>

                    <section>
                        <h2>
                            <FormattedMessage
                                id="forum.albums.sidebar.photos-title"
                                defaultMessage="Photos"
                            />
                        </h2>
                        <div id="photo-list-container">
                            {loading ? (
                                <div className="text-center" id="image-loader">
                                    <i className="fa fa-pulse fa-spinner fa-4x" />
                                </div>
                            ) : null}

                            <PhotoList photos={photos} />
                        </div>

                        <div id="photo-list-pagination" />
                    </section>
                </div>
            </div>

            <div className="lid" onClick={() => setClosed(false)}>
                <i className="fa fa-camera fa-rotate-270 fa-2x" />
            </div>
        </>
    );
};

SideBar.propTypes = {};

export default SideBar;

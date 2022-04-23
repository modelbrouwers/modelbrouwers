import React, { useState, useRef, useEffect } from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";
import classNames from "classnames";
import PerfectScrollbar from "perfect-scrollbar";

import AlbumSelect from "./AlbumSelect";

const SideBar = () => {
    const [closed, setClosed] = useState(true);
    const [albumId, setAlbumId] = useState("");
    const containerRef = useRef(null);
    const className = classNames("box-sizing", {
        closed: closed,
        open: !closed,
    });

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

    console.log(albumId);

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

                        <AlbumSelect onChange={setAlbumId} selected={albumId} />
                    </section>

                    <section>
                        <h2>
                            <FormattedMessage
                                id="forum.albums.sidebar.photos-title"
                                defaultMessage="Photos"
                            />
                        </h2>
                        <div id="photo-list-container">
                            <div className="text-center" id="image-loader">
                                <i className="fa fa-pulse fa-spinner fa-4x" />
                            </div>
                            <ul id="photo-list" />
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

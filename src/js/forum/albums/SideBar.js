import React, { useState } from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";
import classNames from "classnames";

const SideBar = () => {
    const [closed, setClosed] = useState(true);
    const className = classNames("box-sizing", {
        closed: closed,
        open: !closed
    });
    return (
        <>
            <div id="photo-sidebar" className={className}>
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

                        <select name="album">
                            <option value="">TODO</option>
                        </select>
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

            <div className="lid open-close" onClick={() => setClosed(false)}>
                <i className="fa fa-camera fa-rotate-270 fa-2x" />
            </div>
        </>
    );
};

SideBar.propTypes = {};

export default SideBar;

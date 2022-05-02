import React from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";

import Paginator from "../../scripts/paginator";

const NavButton = ({ label, content, onClick }) => (
    <a href="#" aria-label={label} onClick={onClick}>
        <span aria-hidden="true">{content}</span>
    </a>
);

NavButton.propTypes = {
    label: PropTypes.node.isRequired,
    content: PropTypes.string.isRequired,
    onClick: PropTypes.func.isRequired,
};

const PhotosPagination = ({ paginator = null, onPageRequested }) => {
    if (paginator == null) return null;

    const onLinkClick = (pageNr, event) => {
        event.preventDefault();
        onPageRequested(pageNr);
    };

    return (
        <div id="photo-list-pagination">
            <nav className="text-right">
                <ul className="pagination">
                    <li className={paginator.has_previous ? "" : "disabled"}>
                        {paginator.has_previous ? (
                            <NavButton
                                onClick={onLinkClick.bind(
                                    this,
                                    paginator.previous_page_number
                                )}
                                content="&laquo;"
                                label={
                                    <FormattedMessage
                                        id="forum.albums.photosNav.previous"
                                        defaultMessage="Previous"
                                    />
                                }
                            />
                        ) : (
                            <a href="#">
                                <span aria-hidden="true">&laquo;</span>
                            </a>
                        )}
                    </li>

                    {paginator.page_range.map((page) => (
                        <li
                            className={
                                page === paginator.number ? "active" : ""
                            }
                            key={page}
                        >
                            <a href="#" onClick={onLinkClick.bind(this, page)}>
                                {page}
                            </a>
                        </li>
                    ))}

                    <li className={paginator.has_next ? "" : "disabled"}>
                        {paginator.has_next ? (
                            <NavButton
                                onClick={onLinkClick.bind(
                                    this,
                                    paginator.next_page_number
                                )}
                                content="&raquo;"
                                label={
                                    <FormattedMessage
                                        id="forum.albums.photosNav.next"
                                        defaultMessage="Next"
                                    />
                                }
                            />
                        ) : (
                            <a href="#">
                                <span aria-hidden="true">&raquo;</span>
                            </a>
                        )}
                    </li>
                </ul>
            </nav>
        </div>
    );
};

PhotosPagination.propTypes = {
    paginator: PropTypes.instanceOf(Paginator),
    onPageRequested: PropTypes.func.isRequired,
};

export default PhotosPagination;

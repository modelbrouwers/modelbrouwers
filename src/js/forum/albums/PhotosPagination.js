import PropTypes from 'prop-types';
import React from 'react';
import {FormattedMessage} from 'react-intl';

const NavButton = ({label, content, onClick}) => (
  <a href="#" aria-label={label} onClick={onClick}>
    <span aria-hidden="true">{content}</span>
  </a>
);

NavButton.propTypes = {
  label: PropTypes.node.isRequired,
  content: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
};

const PhotosPagination = ({page = 1, numPages = 0, onPageRequested}) => {
  if (numPages < 2) return null;

  const onLinkClick = (pageNr, event) => {
    event.preventDefault();
    onPageRequested(pageNr);
  };

  const hasPrevious = page > 1;
  const hasNext = page < numPages;

  return (
    <div id="photo-list-pagination">
      <nav className="text-right">
        <ul className="pagination">
          <li className={hasPrevious ? '' : 'disabled'}>
            {hasPrevious ? (
              <NavButton
                onClick={event => onLinkClick(page - 1, event)}
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

          {[...Array(numPages).keys()].map(index => {
            const _page = index + 1;
            return (
              <li className={_page === page ? 'active' : ''} key={_page}>
                <a href="#" onClick={event => onLinkClick(_page, event)}>
                  {_page}
                </a>
              </li>
            );
          })}

          <li className={hasNext ? '' : 'disabled'}>
            {hasNext ? (
              <NavButton
                onClick={event => onLinkClick(page + 1, event)}
                content="&raquo;"
                label={<FormattedMessage id="forum.albums.photosNav.next" defaultMessage="Next" />}
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
  page: PropTypes.number.isRequired,
  numPages: PropTypes.number.isRequired,
  onPageRequested: PropTypes.func.isRequired,
};

export default PhotosPagination;

import PropTypes from 'prop-types';
import React from 'react';

import {STATIC} from '../constants';

const THUMB = `${STATIC}/images/thumb.png`;

const Image = ({src, ...extra}) => {
  if (src === '') return null;
  return (
    <img
      src={src}
      onError={event => {
        event.target.onerror = null;
        event.target.src = THUMB;
      }}
      {...extra}
    />
  );
};

Image.propTypes = {
  src: PropTypes.string.isRequired,
};

export default Image;

import PropTypes from 'prop-types';
import React from 'react';

import {DEFAULT_IMAGE} from '../../../constants';

const ProductImage = ({product, ...props}) => (
  <img
    src={product.image || DEFAULT_IMAGE}
    alt={product.name}
    onError={event => {
      event.target.onerror = null;
      event.target.src = DEFAULT_IMAGE;
    }}
    {...props}
  />
);

ProductImage.propTypes = {
  product: PropTypes.shape({
    name: PropTypes.string.isRequired,
    image: PropTypes.string,
  }).isRequired,
};

export default ProductImage;

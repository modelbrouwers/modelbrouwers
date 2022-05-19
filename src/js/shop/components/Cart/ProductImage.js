import React from "react";
import PropTypes from "prop-types";

import { DEFAULT_IMAGE } from "../../../constants";

const ProductImage = ({ product }) => (
    <img src={product.image || DEFAULT_IMAGE} alt={product.name} />
);

ProductImage.propTypes = {
    product: PropTypes.shape({
        name: PropTypes.string.isRequired,
        image: PropTypes.string,
    }).isRequired,
};

export default ProductImage;

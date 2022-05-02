import React, { Fragment } from "react";
import PropTypes from "prop-types";

const Loader = ({ center = false, wrapper: Wrapper = Fragment }) => {
    const wrapperProps = {};
    if (center) {
        Wrapper = "div";
        wrapperProps.className = "text-center";
    }
    return (
        <Wrapper {...wrapperProps}>
            <i className="fa fa-pulse fa-spinner fa-4x" />
        </Wrapper>
    );
};

Loader.propTypes = {
    center: PropTypes.bool,
};

export default Loader;

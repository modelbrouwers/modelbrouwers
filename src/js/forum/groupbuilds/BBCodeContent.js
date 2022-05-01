import React from "react";
import PropTypes from "prop-types";

const BBCodeContent = ({ content, component: Component = "p", ...props }) => {
    return (
        <Component dangerouslySetInnerHTML={{ __html: content }} {...props} />
    );
};

BBCodeContent.propTypes = {
    content: PropTypes.string.isRequired,
    component: PropTypes.oneOfType([PropTypes.string, PropTypes.elementType]),
};

export default BBCodeContent;

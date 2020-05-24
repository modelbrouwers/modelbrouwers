import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";

const Label = ({ label, htmlId, labelGrid = "col-sm-4", required = false }) => {
    const labelClassNames = classNames("control-label", labelGrid, {
        required: required
    });
    return (
        <label
            id={`label_${htmlId}`}
            htmlFor={htmlId}
            className={labelClassNames}
        >
            {label}
        </label>
    );
};

Label.propTypes = {
    label: PropTypes.string.isRequired,
    htmlId: PropTypes.string.isRequired,
    labelGrid: PropTypes.string,
    required: PropTypes.bool
};

export { Label };

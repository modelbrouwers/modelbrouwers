import React from "react";
import PropTypes from "prop-types";

const FAIcon = ({ icon, extra = [] }) => {
    const classNames = ["fa", `fa-${icon}`, ...extra];
    return <i className={classNames.join(" ")} aria-hidden="true" />;
};

FAIcon.propTypes = {
    icon: PropTypes.string.isRequired,
    extra: PropTypes.arrayOf(PropTypes.string),
};

export default FAIcon;

import React from "react";
import PropTypes from "prop-types";

const Yes = () => <i className="fa fa-check" />;
const No = () => <i className="fa fa-times" />;

const YesNo = ({
    children: value,
    yes = <Yes />,
    no = <No />,
    empty = <No />,
}) => {
    if (value == null) return empty;
    return value ? yes : no;
};

YesNo.propTypes = {
    children: PropTypes.bool,
    yes: PropTypes.element,
    no: PropTypes.element,
    empty: PropTypes.element,
};

export default YesNo;

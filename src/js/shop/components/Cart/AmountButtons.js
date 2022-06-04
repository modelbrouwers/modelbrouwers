import React from "react";
import PropTypes from "prop-types";

import FAIcon from "../../../components/FAIcon";

const BaseButton = ({ icon, onClick }) => (
    <button type="button" className="button button--blue" onClick={onClick}>
        <FAIcon icon={icon} />
    </button>
);

BaseButton.propTypes = {
    icon: PropTypes.string.isRequired,
    onClick: PropTypes.func.isRequired,
};

const IncrementButton = ({ onClick }) => (
    <BaseButton icon="plus" onClick={onClick} />
);

IncrementButton.propTypes = {
    onClick: PropTypes.string.isRequired,
};

const DecrementButton = ({ onClick }) => (
    <BaseButton icon="minus" onClick={onClick} />
);

DecrementButton.propTypes = {
    onClick: PropTypes.string.isRequired,
};

export { IncrementButton, DecrementButton };

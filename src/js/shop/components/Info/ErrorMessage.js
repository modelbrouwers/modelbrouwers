import React from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";

/**
 *
 * Info
 *
 */
const ErrorMessage = ({ message = null }) => {
    if (message == null) {
        message = (
            <FormattedMessage
                description="General error message"
                defaultMessage="Oops, something went wrong. Please try again later."
            />
        );
    }

    return <div>{message}</div>;
};

ErrorMessage.propTypes = {
    message: PropTypes.node,
};

export default ErrorMessage;

import React from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";

/**
 *
 * ErrorPage
 *
 */
const ErrorPage = ({ message = null }) => {
    if (message == null) {
        message = (
            <FormattedMessage
                description="General error message"
                defaultMessage="Oops, something went wrong. Please try again later."
            />
        );
    }
    return (
        <div>
            <p>{message}</p>
            <button
                className="button button--blue"
                onClick={() => window.location.reload()}
            >
                <FormattedMessage
                    description="General error: reload page button"
                    defaultMessage="Reload page"
                />
            </button>
        </div>
    );
};

ErrorPage.propTypes = {
    message: PropTypes.node,
};

export default ErrorPage;

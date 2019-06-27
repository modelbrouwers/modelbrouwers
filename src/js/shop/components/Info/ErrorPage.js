import React from "react";
import PropTypes from "prop-types";
import { msg } from "../../../translations/components/Message";
import messages from "./messages";

/**
 *
 * ErrorPage
 *
 */
const ErrorPage = ({ message }) => {
    return (
        <div>
            <p>{msg(message || messages.generalError)}</p>
            <button
                className="button button--blue"
                onClick={() => window.location.reload()}
            >
                {msg(messages.reload)}
            </button>
        </div>
    );
};

ErrorPage.propTypes = {};

export default ErrorPage;

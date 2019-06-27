import React from "react";
import PropTypes from "prop-types";
import { msg } from "../../../translations/components/Message";
import messages from "./messages";

/**
 *
 * Info
 *
 */
const ErrorMessage = ({ message }) => {
    return <div>{msg(message || messages.generalError)}</div>;
};

ErrorMessage.propTypes = {};

export default ErrorMessage;

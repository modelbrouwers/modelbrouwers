import React from "react";
import PropTypes from "prop-types";
import { msg } from "../../../translations/components/Message";
import messages from "./messages";
import { Navigation } from "./index";

/**
 *
 * Checkout
 *
 */
const Checkout = props => {
    return (
        <div className="checkout">
            <h3 className="checkout__header">{msg(messages.checkout)}</h3>
            <div className="checkout__container">
                <Navigation />
            </div>
        </div>
    );
};

Checkout.propTypes = {};

export default Checkout;

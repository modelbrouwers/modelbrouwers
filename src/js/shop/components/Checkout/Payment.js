import React from "react";
import PropTypes from "prop-types";
import { msg } from "../../../translations/components/Message";
import messages from "./messages";
import Address from "./Address";

/**
 *
 * Payment
 *
 */
const Payment = ({ profile }) => {
    return (
        <div className="container">
            <div className="row">
                <h3 className="checkout__title col-xs-12">
                    {msg(messages.selectPaymentMethod)}
                </h3>
            </div>
        </div>
    );
};

Payment.propTypes = {
    profile: PropTypes.object
};

Payment.defaultProps = {
    profile: {}
};

export default Payment;

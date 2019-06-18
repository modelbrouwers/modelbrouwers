import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { msg } from "../../../translations/components/Message";
import messages from "./messages";

/**
 *
 * Payment
 *
 */
const Payment = ({ profile }) => {
    const [paymentMethods, setPaymentMethods] = useState([]);

    useEffect(() => {
        getPaymentMethods();
    });

    const getPaymentMethods = async => {
        try {
        } catch (e) {}
    };
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

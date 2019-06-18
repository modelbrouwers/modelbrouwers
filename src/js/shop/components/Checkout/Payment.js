import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import orderBy from "lodash.orderby";
import { msg } from "../../../translations/components/Message";
import messages from "./messages";
import { PaymentConsumer } from "../../../data/shop/payment";

const paymentConsumer = new PaymentConsumer();
/**
 *
 * Payment
 *
 */
const Payment = ({ profile }) => {
    const [paymentMethods, setPaymentMethods] = useState([]);

    useEffect(() => {
        getPaymentMethods();
    }, []);

    const getPaymentMethods = async () => {
        try {
            const resp = await paymentConsumer.listMethods();
            setPaymentMethods(resp.responseData);
        } catch (e) {
            // TODO Error handling
            console.log(e);
        }
    };
    return (
        <div className="container">
            <div className="row">
                <h3 className="checkout__title ">
                    {msg(messages.selectPaymentMethod)}
                </h3>
            </div>
            <div className="row">
                <div className="col-xs-12">
                    {orderBy(paymentMethods, ["order"], ["asc"]).map(method => (
                        <div className="payment-method__card" key={method.name}>
                            <img
                                className="payment-method__logo"
                                src={method.logo}
                                alt={method.name}
                            />
                        </div>
                    ))}
                </div>
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

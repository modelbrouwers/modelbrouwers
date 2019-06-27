import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import classnames from "classnames";
import orderBy from "lodash.orderby";
import { msg } from "../../../translations/components/Message";
import messages from "./messages";
import { PaymentConsumer } from "../../../data/shop/payment";
import { ErrorMessage } from "../Info";

const paymentConsumer = new PaymentConsumer();
/**
 *
 * Payment
 *
 */
const Payment = ({ profile }) => {
    const [paymentMethods, setPaymentMethods] = useState([]);
    const [paymentMethod, setPaymentMethod] = useState({});
    const [paymentBanks, setPaymentBanks] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(false);

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

    const onMethodClick = async method => {
        setPaymentMethod(method);
        setLoading(true);
        try {
            const resp = await paymentConsumer.listMethodBanks();
            setPaymentBanks(resp.responseData);
        } catch (e) {
            console.log("error", e);
            setError(true);
        } finally {
            setLoading(false);
        }
    };

    const getCardClasses = method => {
        return classnames("payment-method__card", {
            "payment-method__card--active": paymentMethod.id === method.id
        });
    };

    if (error) return <ErrorMessage />;
    return (
        <div className="payment-method__container">
            <div className="payment-method__row">
                <h3 className="checkout__title">
                    {msg(messages.selectPaymentMethod)}
                </h3>
            </div>
            <div className="payment-method__row payment-method__row--logos">
                {orderBy(paymentMethods, ["order"], ["asc"]).map(method => (
                    <div
                        className={getCardClasses(method)}
                        key={method.name}
                        onClick={() => onMethodClick(method)}
                    >
                        <img
                            className="payment-method__logo"
                            src={method.logo}
                            alt={method.name}
                        />
                    </div>
                ))}
            </div>
            {paymentBanks.length
                ? paymentBanks.map(bank => (
                      <div className="payment-method__bank">
                          <p className="payment-method__bank-name">
                              {bank.name}
                          </p>
                      </div>
                  ))
                : null}
            {loading && (
                <div className="loader__container loader--full-width">
                    Loading...
                </div>
            )}
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

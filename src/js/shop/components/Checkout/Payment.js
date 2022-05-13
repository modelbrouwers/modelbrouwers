import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import orderBy from "lodash.orderby";
import { FormattedMessage } from "react-intl";
import useAsync from "react-use/esm/useAsync";

import { PaymentConsumer } from "../../../data/shop/payment";
import Loader from "../../../components/loaders";
import { ErrorMessage } from "../Info";

const paymentConsumer = new PaymentConsumer();

const useFetchPaymentMethods = () => {
    const {
        loading,
        error,
        value = [],
    } = useAsync(async () => {
        const methodList = await paymentConsumer.listMethods();
        return methodList;
    }, []);
    const paymentMethods = orderBy(value, ["order"], ["asc"]);
    return {
        loading,
        error,
        paymentMethods,
    };
};

const PaymentMethod = ({
    id,
    name,
    order,
    logo = null,
    isSelected = false,
    onChange,
}) => {
    const className = classNames("payment-method", {
        "payment-method--has-logo": !!logo,
        "payment-method--active": isSelected,
    });

    return (
        <label className={className}>
            <input
                type="radio"
                className="payment-methods__input payment-methods__input--hidde"
                id={`paymentmethod-${id}`}
                name="paymentMethod"
                value={id}
                onChange={onChange}
                checked={isSelected}
            />
            <div className="payment-method__logo">
                {logo && <img src={logo} alt={name} />}
            </div>
            <span className="payment-method__name">{name}</span>
        </label>
    );
};

PaymentMethod.propTypes = {
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    order: PropTypes.number.isRequired,
    logo: PropTypes.string,
    isSelected: PropTypes.bool,
    onChange: PropTypes.func.isRequired,
};

/**
 *
 * Payment method selection & flow
 *
 */
const Payment = () => {
    const { loading, error, paymentMethods } = useFetchPaymentMethods();
    const [selectedMethod, setSelectedMethod] = useState(null);

    if (error) return <ErrorMessage />;

    return (
        <>
            <h3 className="checkout__title">
                <FormattedMessage
                    description="Checkout: select payment method"
                    defaultMessage="Select your payment method"
                />
            </h3>

            {loading && <Loader />}

            <div className="payment-methods" aria-role="listbox">
                {paymentMethods.map((method) => (
                    <PaymentMethod
                        key={method.id}
                        {...method}
                        isSelected={method.id === selectedMethod}
                        onChange={(event) =>
                            setSelectedMethod(parseInt(event.target.value, 10))
                        }
                    />
                ))}
            </div>
        </>
    );
};

Payment.propTypes = {};

export default Payment;

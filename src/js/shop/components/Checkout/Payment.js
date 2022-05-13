import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import orderBy from "lodash.orderby";
import { FormattedMessage } from "react-intl";
import Select from "react-select";
import useAsync from "react-use/esm/useAsync";

import { PaymentConsumer } from "../../../data/shop/payment";
import Loader from "../../../components/loaders";
import { ErrorMessage } from "../Info";
import { FormField, FormGroup } from "./FormFields";

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

const useGetPaymentSpecificOptions = (paymentMethod) => {
    const {
        loading,
        error,
        value = {},
    } = useAsync(async () => {
        if (!paymentMethod) return;

        switch (paymentMethod.name.toLowerCase()) {
            case "ideal": {
                const idealBanks = await paymentConsumer.listIdealBanks();
                return { banks: idealBanks.responseData };
            }
        }
    }, [paymentMethod]);

    if (error) {
        throw error;
    }

    return value;
};

const PaymentMethodSpecificOptions = ({
    paymentMethod,
    paymentMethodSpecificState,
    setPaymentMethodSpecificState,
    ...props
}) => {
    if (!paymentMethod) return null;

    switch (paymentMethod.name.toLowerCase()) {
        case "ideal": {
            const { banks } = props;
            if (!banks) return <Loader />;

            const onBankChange = (bank) => {
                setPaymentMethodSpecificState({
                    ...paymentMethodSpecificState,
                    bank: bank,
                });
            };

            return (
                <>
                    <div className="spacer" />
                    <FormGroup>
                        <FormField
                            name="bank"
                            label={
                                <FormattedMessage
                                    description="iDeal bank dropdown"
                                    defaultMessage="Select your bank"
                                />
                            }
                            required
                            component={Select}
                            value={paymentMethodSpecificState.bank}
                            options={banks.map((bank) => ({
                                value: bank.id,
                                label: bank.name,
                            }))}
                            onChange={onBankChange}
                            className=""
                            autoFocus={!paymentMethodSpecificState.bank}
                        />
                    </FormGroup>
                </>
            );
        }
    }

    return null;
};

PaymentMethodSpecificOptions.propTypes = {
    paymentMethod: PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
        order: PropTypes.number.isRequired,
        logo: PropTypes.string,
    }),
};

/**
 *
 * Payment method selection & flow
 *
 */
const Payment = () => {
    const { loading, error, paymentMethods } = useFetchPaymentMethods();
    const [selectedMethod, setSelectedMethod] = useState(null);
    const [paymentMethodSpecificState, setPaymentMethodSpecificState] =
        useState({});
    const paymentMethod = paymentMethods.find(
        (method) => method.id === selectedMethod
    );
    const paymentMethodOptions = useGetPaymentSpecificOptions(paymentMethod);

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

            <div className="payment-methods">
                {paymentMethods.map((method) => (
                    <PaymentMethod
                        key={method.id}
                        {...method}
                        isSelected={
                            paymentMethod && method.id === paymentMethod.id
                        }
                        onChange={(event) =>
                            setSelectedMethod(parseInt(event.target.value, 10))
                        }
                    />
                ))}
            </div>

            <PaymentMethodSpecificOptions
                paymentMethod={paymentMethod}
                paymentMethodSpecificState={paymentMethodSpecificState}
                setPaymentMethodSpecificState={setPaymentMethodSpecificState}
                {...paymentMethodOptions}
            />
        </>
    );
};

Payment.propTypes = {};

export default Payment;

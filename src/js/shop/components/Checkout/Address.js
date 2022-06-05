import React, { useState } from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";
import Select from "react-select";
import { useNavigate } from "react-router-dom";

import { country_list, SUPPORTED_COUNTRIES, EMPTY_ADDRESS } from "./constants";
import AddressFields from "./AddressFields";
import PersonalDetailsFields from "./PersonalDetailsFields";

const AddressType = PropTypes.shape({
    company: PropTypes.string,
    chamberOfCommerce: PropTypes.string,
    street: PropTypes.string,
    number: PropTypes.string,
    city: PropTypes.string,
    postalCode: PropTypes.string,
    country: PropTypes.string,
});

const CustomerType = PropTypes.shape({
    firstName: PropTypes.string,
    lastName: PropTypes.string,
    email: PropTypes.string,
    phone: PropTypes.string,
});

/**
 *
 * Address
 *
 */
const Address = ({
    customer,
    deliveryAddress,
    billingAddress,
    allowSubmit = false,
    onChange,
}) => {
    const [
        deliveryAddressIsBillingAddress,
        setDeliveryAddressIsBillingAddress,
    ] = useState(true);
    const navigate = useNavigate();

    // TODO this probably needs to send api request to create/modify an order
    const onSubmit = (event) => {
        event.preventDefault();
        navigate("/payment");
        return;
    };

    billingAddress =
        billingAddress ??
        (!deliveryAddressIsBillingAddress ? EMPTY_ADDRESS : null);

    return (
        <form onSubmit={onSubmit}>
            <div className="row">
                {/*Personal details*/}
                <div className="col-xs-12 col-md-6">
                    <h3 className="checkout__title">
                        <FormattedMessage
                            description="Checkout address: personal details"
                            defaultMessage="Personal details"
                        />
                    </h3>

                    <PersonalDetailsFields
                        prefix="customer"
                        firstName={customer.firstName}
                        lastName={customer.lastName}
                        email={customer.email}
                        phone={customer.phone}
                        onChange={onChange}
                    />
                </div>
            </div>

            <div className="row">
                {/*Delivery address*/}
                <div className="col-md-6 col-xs-12">
                    <h3 className="checkout__title">
                        <FormattedMessage
                            description="Delivery address: deliveryAddress"
                            defaultMessage="Delivery address"
                        />
                    </h3>

                    <AddressFields
                        prefix="deliveryAddress"
                        company={deliveryAddress.company}
                        chamberOfCommerce={deliveryAddress.chamberOfCommerce}
                        street={deliveryAddress.street}
                        number={deliveryAddress.number}
                        city={deliveryAddress.city}
                        postalCode={deliveryAddress.postalCode}
                        country={{
                            value: deliveryAddress.country,
                            label: SUPPORTED_COUNTRIES[deliveryAddress.country],
                        }}
                        onChange={onChange}
                    />

                    <div className="form-check checkbox-flex">
                        <input
                            type="checkbox"
                            className="form-check-input"
                            id="deliveryAddressIsBillingAddress"
                            checked={deliveryAddressIsBillingAddress}
                            onChange={() => {
                                setDeliveryAddressIsBillingAddress(
                                    !deliveryAddressIsBillingAddress
                                );
                                onChange({
                                    target: {
                                        name: "billingAddress",
                                        value: null,
                                    },
                                });
                            }}
                        />
                        <label
                            className="form-check-label"
                            htmlFor="deliveryAddressIsBillingAddress"
                        >
                            <FormattedMessage
                                description="Checkout address: billingAddressSame"
                                defaultMessage="My billing and delivery address are the same."
                            />
                        </label>
                    </div>
                </div>

                {/*Billing address*/}
                {!deliveryAddressIsBillingAddress && (
                    <div className="col-md-6 col-xs-12">
                        <h3 className="checkout__title">
                            <FormattedMessage
                                description="Billing address: billingAddress"
                                defaultMessage="Billing address"
                            />
                        </h3>

                        {/* TODO: fix default country being reset */}
                        <AddressFields
                            prefix="billingAddress"
                            company={billingAddress.company}
                            chamberOfCommerce={billingAddress.chamberOfCommerce}
                            street={billingAddress.street}
                            number={billingAddress.number}
                            city={billingAddress.city}
                            postalCode={billingAddress.postalCode}
                            country={{
                                value: billingAddress.country,
                                label: SUPPORTED_COUNTRIES[
                                    billingAddress.country
                                ],
                            }}
                            onChange={onChange}
                        />
                    </div>
                )}
            </div>

            <div className="spacer" />
            <div>
                <small className="checkout__help-text">
                    *{" "}
                    <FormattedMessage
                        description="Checkout address: requiredFields"
                        defaultMessage="Required fields"
                    />
                </small>
                <button
                    type="submit"
                    className="button button--blue pull-right"
                    disabled={!allowSubmit}
                >
                    <FormattedMessage
                        description="Checkout address: continue"
                        defaultMessage="Continue"
                    />
                </button>
            </div>
        </form>
    );
};

Address.propTypes = {
    customer: CustomerType,
    deliveryAddress: AddressType.isRequired,
    billingAddress: AddressType,
    onChange: PropTypes.func.isRequired,
    allowSubmit: PropTypes.bool,
};

export default Address;

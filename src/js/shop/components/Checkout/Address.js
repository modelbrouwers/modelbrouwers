import React, { useState } from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";
import Select from "react-select";
import { useNavigate } from "react-router-dom";

import { country_list, SUPPORTED_COUNTRIES } from "./constants";

/**
 *
 * Address
 *
 */
const Address = ({ user }) => {
    // Set default values for missing fields to avoid null errors
    const defaultUser = { profile: {}, kvk: "", company: "" };
    const [userDetails, setUserDetails] = useState({
        ...defaultUser,
        ...user,
    });
    const [addressCheck, setAddressCheck] = useState(true);
    const [billingDetails, setBillingDetails] = useState({});
    const mandatoryUserFields = ["first_name", "last_name", "email"];
    const mandatoryProfileFields = [
        "street",
        "number",
        "city",
        "country",
        "postal",
    ];

    /**
     * Disable 'Continue' button if any of the required fields is empty/null
     */
    const requiredFieldMissing = () => {
        return (
            mandatoryUserFields.some((field) => !userDetails[field]) ||
            mandatoryProfileFields.some((field) => !userDetails[field])
        );
    };

    const onProfileChange = (e) => {
        const { name, value } = e.target;
        setUserDetails({ ...userDetails, [name]: value });
    };

    const onBillingDetailsChange = (e) => {
        const { name, value } = e.target;
        setBillingDetails({ ...billingDetails, [name]: value });
    };

    // Separate handler to update user data
    const onUserChange = (e) => {
        const { name, value } = e.target;
        setUserDetails({
            ...userDetails,
            user: { ...userDetails, [name]: value },
        });
    };

    // Separate onchange handlers for selects, since data repr is different there
    const onCountryChange = (country) => {
        setUserDetails((user) => ({ ...user, country: country.value }));
    };

    const onBillingCountryChange = (country) => {
        setBillingDetails((details) => ({
            ...details,
            country: country.value,
        }));
    };

    // TODO this probably needs to send api request to create/modify an order
    const onAddressComplete = () => {
        useNavigate("/payment");
        return;
    };

    return (
        <div className="container">
            <div className="row">
                {/*Personal details*/}
                <div className="col-xs-12">
                    <div className="row">
                        <div className="col-xs-6">
                            <h3 className="checkout__title col-xs-12">
                                <FormattedMessage
                                    description="Checkout address: personal details"
                                    defaultMessage="Personal details"
                                />
                            </h3>
                            <div className="form-group col-md-6 col-xs-12">
                                <label className="control-label">
                                    <FormattedMessage
                                        description="Checkout address: firstName"
                                        defaultMessage="First name"
                                    />
                                    *
                                </label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={userDetails.first_name}
                                    name="first_name"
                                    onChange={onUserChange}
                                />
                            </div>
                            <div className="form-group col-md-6 col-xs-12">
                                <label className="control-label">
                                    <FormattedMessage
                                        description="Checkout address: lastName"
                                        defaultMessage="Last name"
                                    />
                                    *
                                </label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={userDetails.last_name}
                                    name="last_name"
                                    onChange={onUserChange}
                                />
                            </div>

                            <div className="form-group col-xs-12">
                                <label className="control-label">
                                    <FormattedMessage
                                        description="Checkout address: email"
                                        defaultMessage="Email address"
                                    />
                                    *
                                </label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={userDetails.email}
                                    name="email"
                                    onChange={onUserChange}
                                />
                            </div>

                            <div className="form-group col-xs-12">
                                <label className="control-label">
                                    <FormattedMessage
                                        description="Checkout address: phone"
                                        defaultMessage="Phone number"
                                    />
                                </label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={userDetails.phone}
                                    name="phone"
                                    onChange={onUserChange}
                                />
                            </div>
                        </div>
                    </div>
                </div>

                {/*Delivery address*/}
                <div className="col-md-6 col-xs-12">
                    <h3 className="checkout__title col-xs-12">
                        <FormattedMessage
                            description="Delivery address: deliveryAddress"
                            defaultMessage="Delivery address"
                        />
                    </h3>
                    <div className="form-group col-xs-12">
                        <label className="control-label">
                            <FormattedMessage
                                description="Delivery address: company"
                                defaultMessage="Company"
                            />
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={userDetails.company}
                            name="company"
                            onChange={onProfileChange}
                        />
                    </div>
                    <div className="form-group col-xs-12">
                        <label className="control-label">
                            <FormattedMessage
                                description="Delivery address: kvk"
                                defaultMessage="KVK"
                            />
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={userDetails.kvk}
                            name="kvk"
                            onChange={onProfileChange}
                        />
                    </div>
                    <div className="form-group col-xs-12">
                        <label className="control-label">
                            <FormattedMessage
                                description="Delivery address: street"
                                defaultMessage="Street"
                            />
                            *
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={userDetails.profile.street}
                            name="street"
                            onChange={onProfileChange}
                        />
                    </div>
                    <div className="form-group col-xs-12">
                        <label className="control-label">
                            <FormattedMessage
                                description="Delivery address: number"
                                defaultMessage="Number"
                            />
                            *
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={userDetails.profile.number}
                            name="number"
                            onChange={onProfileChange}
                        />
                    </div>
                    <div className="form-group col-md-6 col-xs-12">
                        <label className="control-label">
                            <FormattedMessage
                                description="Delivery address: city"
                                defaultMessage="City"
                            />
                            *
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={userDetails.profile.city}
                            name="city"
                            onChange={onProfileChange}
                        />
                    </div>
                    <div className="form-group col-md-6 col-xs-12">
                        <label className="control-label">
                            <FormattedMessage
                                description="Delivery address: zip"
                                defaultMessage="ZIP code"
                            />
                            *
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={userDetails.profile.postal}
                            name="postal"
                            onChange={onProfileChange}
                        />
                    </div>
                    <div className="form-group col-xs-12">
                        <label className="control-label">
                            <FormattedMessage
                                description="Checkout address: country"
                                defaultMessage="Country"
                            />
                            *
                        </label>
                        <Select
                            name="country"
                            value={{
                                value: userDetails.profile.country || "",
                                label: SUPPORTED_COUNTRIES[userDetails.country],
                            }}
                            options={country_list}
                            onChange={onCountryChange}
                            placeholder={
                                <FormattedMessage
                                    description="Country dropdown placeholder"
                                    defaultMessage="Select country"
                                />
                            }
                        />
                    </div>
                    <div className="form-check col-xs-12 checkbox-flex">
                        <input
                            type="checkbox"
                            className="form-check-input"
                            id="addressCheck"
                            checked={addressCheck}
                            onChange={() => setAddressCheck(!addressCheck)}
                        />
                        <label
                            className="form-check-label"
                            htmlFor="addressCheck"
                        >
                            <FormattedMessage
                                description="Checkout address: billingAddressSame"
                                defaultMessage="My billing and delivery address are the same."
                            />
                        </label>
                    </div>
                </div>

                {/*Billing address*/}
                {!addressCheck && (
                    <div className="col-md-6 col-xs-12">
                        <h3 className="checkout__title col-xs-12">
                            <FormattedMessage
                                description="Billing address: billingAddress"
                                defaultMessage="Billing address"
                            />
                        </h3>
                        <div className="form-group col-xs-12">
                            <label className="control-label">
                                <FormattedMessage
                                    description="Billing address: company"
                                    defaultMessage="Company"
                                />
                            </label>
                            <input
                                type="text"
                                className="form-control"
                                value={billingDetails.company}
                                name="company"
                                onChange={onBillingDetailsChange}
                            />
                        </div>
                        <div className="form-group col-xs-12">
                            <label className="control-label">
                                <FormattedMessage
                                    description="Billing address: kvk"
                                    defaultMessage="KVK"
                                />
                            </label>
                            <input
                                type="text"
                                className="form-control"
                                value={billingDetails.kvk}
                                name="kvk"
                                onChange={onBillingDetailsChange}
                            />
                        </div>
                        <div className="form-group col-xs-12">
                            <label className="control-label">
                                <FormattedMessage
                                    description="Billing address: street"
                                    defaultMessage="Street"
                                />
                                *
                            </label>
                            <input
                                type="text"
                                className="form-control"
                                value={billingDetails.street}
                                name="street"
                                onChange={onBillingDetailsChange}
                            />
                        </div>
                        <div className="form-group col-xs-12">
                            <label className="control-label">
                                <FormattedMessage
                                    description="Billing address: number"
                                    defaultMessage="Number"
                                />
                                *
                            </label>
                            <input
                                type="text"
                                className="form-control"
                                value={billingDetails.number}
                                name="number"
                                onChange={onBillingDetailsChange}
                            />
                        </div>
                        <div className="form-group col-md-6 col-xs-12">
                            <label className="control-label">
                                <FormattedMessage
                                    description="Billing address: city"
                                    defaultMessage="City"
                                />
                                *
                            </label>
                            <input
                                type="text"
                                className="form-control"
                                value={billingDetails.city}
                                name="city"
                                onChange={onBillingDetailsChange}
                            />
                        </div>
                        <div className="form-group col-md-6 col-xs-12">
                            <label className="control-label">
                                <FormattedMessage
                                    description="Billing address: zip"
                                    defaultMessage="ZIP code"
                                />
                            </label>
                            <input
                                type="text"
                                className="form-control"
                                value={billingDetails.postal}
                                name="postal"
                                onChange={onBillingDetailsChange}
                            />
                        </div>
                        <div className="form-group col-xs-12">
                            <label className="control-label">
                                <FormattedMessage
                                    description="Billing address: country"
                                    defaultMessage="Country"
                                />
                                *
                            </label>

                            <Select
                                name="country"
                                value={{
                                    value: billingDetails.country || "",
                                    label: SUPPORTED_COUNTRIES[
                                        billingDetails.country
                                    ],
                                }}
                                options={country_list}
                                onChange={onBillingCountryChange}
                                placeholder={
                                    <FormattedMessage
                                        description="Country dropdown placeholder"
                                        defaultMessage="Select country"
                                    />
                                }
                            />
                        </div>
                    </div>
                )}
            </div>
            <div className="col-xs-12">
                <div className="spacer" />
                <small className="checkout__help-text">
                    *{" "}
                    <FormattedMessage
                        description="Checkout address: requiredFields"
                        defaultMessage="Required fields"
                    />
                </small>
                <button
                    className={"button button--blue"}
                    disabled={requiredFieldMissing()}
                    onClick={onAddressComplete}
                >
                    <FormattedMessage
                        description="Checkout address: continue"
                        defaultMessage="Continue"
                    />
                </button>
            </div>
        </div>
    );
};

Address.propTypes = {
    user: PropTypes.object,
};

export default Address;

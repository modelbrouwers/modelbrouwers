import React, { useState } from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { msg } from "../../../translations/components/Message";
import messages from "./messages";

/**
 *
 * Address
 *
 */
const Address = ({ profile }) => {
    // Set default values for missing fields to avoid null errors
    const defaultProfile = { user: {}, kvk: "", company: "" };
    const [userDetails, setUserDetails] = useState({
        ...defaultProfile,
        ...profile
    });
    const [addressCheck, setAddressCheck] = useState(true);
    const [billingDetails, setBillingDetails] = useState({});

    const onProfileChange = e => {
        const { name, value } = e.target;
        setUserDetails({ ...userDetails, [name]: value });
    };

    const onBillingDetailsChange = e => {
        const { name, value } = e.target;
        setBillingDetails({ ...billingDetails, [name]: value });
    };

    // Separate handler to update user data
    const onUserChange = e => {
        const { name, value } = e.target;
        setUserDetails({
            ...userDetails,
            user: { ...userDetails.user, [name]: value }
        });
    };
    return (
        <div className="container">
            <div className="row">
                {/*Personal details*/}
                <div className="col-xs-12">
                    <div className="row">
                        <div className="col-xs-6">
                            <h3 className="checkout__title col-xs-12">
                                {msg(messages.personalDetails)}
                            </h3>
                            <div className="form-group col-md-6 col-xs-12">
                                <label className="control-label">
                                    {msg(messages.firstName)}
                                </label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={userDetails.user.first_name}
                                    name="first_name"
                                    onChange={onUserChange}
                                />
                            </div>
                            <div className="form-group col-md-6 col-xs-12">
                                <label className="control-label">
                                    {msg(messages.lastName)}
                                </label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={userDetails.user.last_name}
                                    name="last_name"
                                    onChange={onUserChange}
                                />
                            </div>

                            <div className="form-group col-xs-12">
                                <label className="control-label">
                                    {msg(messages.email)}
                                </label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={userDetails.user.email}
                                    name="email"
                                    onChange={onUserChange}
                                />
                            </div>

                            <div className="form-group col-xs-12">
                                <label className="control-label">
                                    {msg(messages.phone)}
                                </label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={userDetails.user.phone}
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
                        {msg(messages.deliveryAddress)}
                    </h3>
                    <div className="form-group col-xs-12">
                        <label className="control-label">
                            {msg(messages.company)}
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
                            {msg(messages.kvk)}
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
                            {msg(messages.street)}
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={userDetails.street}
                            name="street"
                            onChange={onProfileChange}
                        />
                    </div>
                    <div className="form-group col-xs-12">
                        <label className="control-label">
                            {msg(messages.number)}
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={userDetails.number}
                            name="number"
                            onChange={onProfileChange}
                        />
                    </div>
                    <div className="form-group col-md-6 col-xs-12">
                        <label className="control-label">
                            {msg(messages.city)}
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={userDetails.city}
                            name="city"
                            onChange={onProfileChange}
                        />
                    </div>
                    <div className="form-group col-md-6 col-xs-12">
                        <label className="control-label">
                            {msg(messages.zip)}
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={userDetails.postal}
                            name="postal"
                            onChange={onProfileChange}
                        />
                    </div>
                    <div className="form-group col-xs-12">
                        <label className="control-label">
                            {msg(messages.country)}
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={userDetails.country}
                            name="country"
                            onChange={onProfileChange}
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
                            {msg(messages.billingAddressSame)}
                        </label>
                    </div>
                </div>

                {/*Billing address*/}
                {!addressCheck && (
                    <div className="col-md-6 col-xs-12">
                        <h3 className="checkout__title col-xs-12">
                            {msg(messages.billingAddress)}
                        </h3>
                        <div className="form-group col-xs-12">
                            <label className="control-label">
                                {msg(messages.company)}
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
                                {msg(messages.kvk)}
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
                                {msg(messages.street)}
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
                                {msg(messages.number)}
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
                                {msg(messages.city)}
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
                                {msg(messages.zip)}
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
                                {msg(messages.country)}
                            </label>
                            <input
                                type="text"
                                className="form-control"
                                value={billingDetails.country}
                                name="country"
                                onChange={onBillingDetailsChange}
                            />
                        </div>
                    </div>
                )}
            </div>
            <div className="spacer" />
            <Link to={`/payment`} className="button button--blue">
                {msg(messages.continue)}
            </Link>
        </div>
    );
};

Address.propTypes = {
    profile: PropTypes.object
};

Address.defaultProps = {
    profile: {}
};

export default Address;

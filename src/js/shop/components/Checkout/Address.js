import React, { useState } from "react";
import PropTypes from "prop-types";
import { msg } from "../../../translations/components/Message";
import messages from "./messages";

/**
 *
 * Address
 *
 */
const Address = ({ user }) => {
    const [userDetails, setUserDetails] = useState(user);
    const [addressCheck, setAddressCheck] = useState(true);

    const onChange = e => {
        const { name, value } = e.target;
        setUserDetails({ ...userDetails, [name]: value });
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
                                    value={user.firstName}
                                    name="firstName"
                                    onChange={onChange}
                                />
                            </div>
                            <div className="form-group col-md-6 col-xs-12">
                                <label className="control-label">
                                    {msg(messages.lastName)}
                                </label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={user.lastName}
                                    name="lastName"
                                    onChange={onChange}
                                />
                            </div>

                            <div className="form-group col-xs-12">
                                <label className="control-label">
                                    {msg(messages.email)}
                                </label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={user.email}
                                    name="email"
                                    onChange={onChange}
                                />
                            </div>

                            <div className="form-group col-xs-12">
                                <label className="control-label">
                                    {msg(messages.phone)}
                                </label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={user.phone}
                                    name="phone"
                                    onChange={onChange}
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
                            value={user.company}
                            name="company"
                            onChange={onChange}
                        />
                    </div>
                    <div className="form-group col-xs-12">
                        <label className="control-label">
                            {msg(messages.kvk)}
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={user.kvk}
                            name="kvk"
                            onChange={onChange}
                        />
                    </div>
                    <div className="form-group col-xs-12">
                        <label className="control-label">
                            {msg(messages.address1)}
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={user.address1}
                            name="address1"
                            onChange={onChange}
                        />
                    </div>
                    <div className="form-group col-xs-12">
                        <label className="control-label">
                            {msg(messages.address2)}
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={user.address2}
                            name="address2"
                            onChange={onChange}
                        />
                    </div>
                    <div className="form-group col-md-6 col-xs-12">
                        <label className="control-label">
                            {msg(messages.city)}
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={user.city}
                            name="city"
                            onChange={onChange}
                        />
                    </div>
                    <div className="form-group col-md-6 col-xs-12">
                        <label className="control-label">
                            {msg(messages.zip)}
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={user.zip}
                            name="zip"
                            onChange={onChange}
                        />
                    </div>
                    <div className="form-group col-xs-12">
                        <label className="control-label">
                            {msg(messages.country)}
                        </label>
                        <input
                            type="text"
                            className="form-control"
                            value={user.country}
                            name="country"
                            onChange={onChange}
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
                                value={user.company}
                                name="company"
                                onChange={onChange}
                            />
                        </div>
                        <div className="form-group col-xs-12">
                            <label className="control-label">
                                {msg(messages.kvk)}
                            </label>
                            <input
                                type="text"
                                className="form-control"
                                value={user.kvk}
                                name="kvk"
                                onChange={onChange}
                            />
                        </div>
                        <div className="form-group col-xs-12">
                            <label className="control-label">
                                {msg(messages.address1)}
                            </label>
                            <input
                                type="text"
                                className="form-control"
                                value={user.address1}
                                name="address1"
                                onChange={onChange}
                            />
                        </div>
                        <div className="form-group col-xs-12">
                            <label className="control-label">
                                {msg(messages.address2)}
                            </label>
                            <input
                                type="text"
                                className="form-control"
                                value={user.address2}
                                name="address2"
                                onChange={onChange}
                            />
                        </div>
                        <div className="form-group col-md-6 col-xs-12">
                            <label className="control-label">
                                {msg(messages.city)}
                            </label>
                            <input
                                type="text"
                                className="form-control"
                                value={user.city}
                                name="city"
                                onChange={onChange}
                            />
                        </div>
                        <div className="form-group col-md-6 col-xs-12">
                            <label className="control-label">
                                {msg(messages.zip)}
                            </label>
                            <input
                                type="text"
                                className="form-control"
                                value={user.zip}
                                name="zip"
                                onChange={onChange}
                            />
                        </div>
                        <div className="form-group col-xs-12">
                            <label className="control-label">
                                {msg(messages.country)}
                            </label>
                            <input
                                type="text"
                                className="form-control"
                                value={user.country}
                                name="country"
                                onChange={onChange}
                            />
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

Address.propTypes = {
    user: PropTypes.object
};

Address.defaultProps = {
    user: {}
};

export default Address;

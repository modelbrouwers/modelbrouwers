import React from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";

import { FormField, FormGroup } from "./FormFields";

const PersonalDetailsFields = ({
    prefix,
    firstName = "",
    lastName = "",
    email = "",
    phone = "",
    onChange,
}) => {
    prefix = prefix ? `${prefix}.` : "";

    return (
        <>
            <div className="row">
                <FormGroup extraClassName="col-md-6 col-xs-12">
                    <FormField
                        name={`${prefix}firstName`}
                        label={
                            <FormattedMessage
                                description="Checkout address: firstName"
                                defaultMessage="First name"
                            />
                        }
                        value={firstName}
                        onChange={onChange}
                        autoFocus={!firstName}
                        required
                    />
                </FormGroup>

                <FormGroup extraClassName="col-md-6 col-xs-12">
                    <FormField
                        name={`${prefix}lastName`}
                        label={
                            <FormattedMessage
                                description="Checkout address: lastName"
                                defaultMessage="Last name"
                            />
                        }
                        value={lastName}
                        onChange={onChange}
                        required
                    />
                </FormGroup>
            </div>

            <FormGroup>
                <FormField
                    name={`${prefix}email`}
                    label={
                        <FormattedMessage
                            description="Checkout address: email"
                            defaultMessage="Email address"
                        />
                    }
                    value={email}
                    onChange={onChange}
                    required
                />
            </FormGroup>

            <FormGroup>
                <FormField
                    name={`${prefix}phone`}
                    label={
                        <FormattedMessage
                            description="Checkout address: phone"
                            defaultMessage="Phone number"
                        />
                    }
                    value={phone}
                    onChange={onChange}
                />
            </FormGroup>
        </>
    );
};

PersonalDetailsFields.propTypes = {
    prefix: PropTypes.string,
    firstName: PropTypes.string,
    lastName: PropTypes.string,
    email: PropTypes.string,
    phone: PropTypes.string,
    onChange: PropTypes.func.isRequired,
};

export default PersonalDetailsFields;

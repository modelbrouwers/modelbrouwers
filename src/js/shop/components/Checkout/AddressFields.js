import isObject from "lodash.isobject";
import React from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";
import Select from "react-select";
import { country_list, SUPPORTED_COUNTRIES } from "./constants";

import { FormField, FormGroup } from "./FormFields";

const AddressFields = ({
    prefix,
    company = "",
    chamberOfCommerce = "",
    street = "",
    number = "",
    city = "",
    postalCode = "",
    country,
    onChange,
}) => {
    prefix = prefix ? `${prefix}.` : "";

    // null or empty object
    if (!country || (isObject(country) && Object.keys(country).length < 2)) {
        country = { value: "", label: "" };
    }

    const onCountryChange = (country, actionMeta) => {
        const { value } = country;
        const { name } = actionMeta;
        onChange({ target: { name, value } });
    };

    return (
        <>
            <FormGroup>
                <FormField
                    name={`${prefix}company`}
                    label={
                        <FormattedMessage
                            description="Delivery address: company"
                            defaultMessage="Company"
                        />
                    }
                    value={company}
                    onChange={onChange}
                />
            </FormGroup>
            <FormGroup>
                <FormField
                    name={`${prefix}chamberOfCommerce`}
                    label={
                        <FormattedMessage
                            description="Delivery address: kvk"
                            defaultMessage="KVK"
                        />
                    }
                    value={chamberOfCommerce}
                    onChange={onChange}
                />
            </FormGroup>
            <FormGroup>
                <FormField
                    name={`${prefix}street`}
                    label={
                        <FormattedMessage
                            description="Delivery address: street"
                            defaultMessage="Street"
                        />
                    }
                    value={street}
                    required
                    onChange={onChange}
                />
            </FormGroup>
            <FormGroup>
                <FormField
                    name={`${prefix}number`}
                    label={
                        <FormattedMessage
                            description="Delivery address: number"
                            defaultMessage="Number"
                        />
                    }
                    value={number}
                    required
                    onChange={onChange}
                />
            </FormGroup>
            <FormGroup>
                <FormField
                    name={`${prefix}city`}
                    label={
                        <FormattedMessage
                            description="Delivery address: city"
                            defaultMessage="City"
                        />
                    }
                    value={city}
                    required
                    onChange={onChange}
                />
            </FormGroup>
            <FormGroup>
                <FormField
                    name={`${prefix}postalCode`}
                    label={
                        <FormattedMessage
                            description="Delivery address: zip"
                            defaultMessage="ZIP code"
                        />
                    }
                    value={postalCode}
                    required
                    onChange={onChange}
                />
            </FormGroup>
            <FormGroup>
                <FormField
                    name={`${prefix}country`}
                    label={
                        <FormattedMessage
                            description="Checkout address: country"
                            defaultMessage="Country"
                        />
                    }
                    value={country}
                    required
                    onChange={onCountryChange}
                    component={Select}
                    options={country_list}
                    placeholder={
                        <FormattedMessage
                            description="Country dropdown placeholder"
                            defaultMessage="Select country"
                        />
                    }
                    className=""
                />
            </FormGroup>
        </>
    );
};

AddressFields.propTypes = {
    prefix: PropTypes.string,
    company: PropTypes.string,
    chamberOfCommerce: PropTypes.string,
    street: PropTypes.string,
    number: PropTypes.string,
    city: PropTypes.string,
    postalCode: PropTypes.string,
    country: PropTypes.shape({
        value: PropTypes.string,
        label: PropTypes.string,
    }),
    onChange: PropTypes.func.isRequired,
};

export default AddressFields;

import isObject from "lodash.isobject";
import React from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";
import Select from "react-select";
import { country_list, SUPPORTED_COUNTRIES } from "./constants";

import { FormField } from "./FormFields";
import TextField from "@/forms/TextField";
import ErrorList from "@/forms/ErrorList";
import FormGroup from "@/forms/FormGroup";

const AddressFields = ({ prefix, country, onChange }) => {
  if (!prefix) throw new Error("Prefix must be non-empty string");

  // null or empty object
  if (!country || (isObject(country) && Object.keys(country).length < 2)) {
    country = { value: "", label: "" };
  }

  return (
    <>
      <TextField
        name={`${prefix}.company`}
        label={
          <FormattedMessage
            description="Delivery address: company"
            defaultMessage="Company"
          />
        }
      />
      <TextField
        name={`${prefix}.chamberOfCommerce`}
        label={
          <FormattedMessage
            description="Delivery address: kvk"
            defaultMessage="KVK"
          />
        }
      />
      <TextField
        name={`${prefix}.street`}
        label={
          <FormattedMessage
            description="Delivery address: street"
            defaultMessage="Street"
          />
        }
        required
      />
      <TextField
        name={`${prefix}.number`}
        label={
          <FormattedMessage
            description="Delivery address: number"
            defaultMessage="Number"
          />
        }
        required
      />
      <TextField
        name={`${prefix}.city`}
        label={
          <FormattedMessage
            description="Delivery address: city"
            defaultMessage="City"
          />
        }
        required
      />
      <TextField
        name={`${prefix}.postalCode`}
        label={
          <FormattedMessage
            description="Delivery address: zip"
            defaultMessage="ZIP code"
          />
        }
        required
      />
      <FormGroup>
        <FormField
          name={`${prefix}.country`}
          label={
            <FormattedMessage
              description="Checkout address: country"
              defaultMessage="Country"
            />
          }
          value={country}
          required
          onChange={(country, actionMeta) => {
            const { value } = country;
            const { name } = actionMeta;
            onChange({ target: { name, value } });
          }}
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
        <ErrorList name={`${prefix}.country`} />
      </FormGroup>
    </>
  );
};

AddressFields.propTypes = {
  prefix: PropTypes.string,
  country: PropTypes.shape({
    value: PropTypes.string,
    label: PropTypes.string,
  }),
  onChange: PropTypes.func.isRequired,
};

export default AddressFields;

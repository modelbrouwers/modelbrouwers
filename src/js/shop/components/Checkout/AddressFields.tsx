import React from "react";
import { FormattedMessage } from "react-intl";

import TextField from "@/components/forms/TextField";
import CountryField from "@/components/forms/CountryField";

export interface AddressFieldsProps {
  prefix: string extends "" ? never : string;
}

const AddressFields: React.FC<AddressFieldsProps> = ({ prefix }) => (
  <>
    <CountryField
      name={`${prefix}.country`}
      label={
        <FormattedMessage
          description="Checkout address: country"
          defaultMessage="Country"
        />
      }
      required
      placeholder={
        <FormattedMessage
          description="Country dropdown placeholder"
          defaultMessage="Select country"
        />
      }
    />
    <div className="row">
      <div className="col-xs-12 col-md-6">
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
      </div>
      <div className="col-xs-12 col-md-6">
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
      </div>
    </div>
    <div className="row">
      <div className="col-xs-12 col-md-6">
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
      </div>
      <div className="col-xs-12 col-md-6">
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
      </div>
    </div>
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
  </>
);

export default AddressFields;

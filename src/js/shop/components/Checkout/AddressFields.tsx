import React from 'react';
import {FormattedMessage} from 'react-intl';

import CountryField from '@/components/forms/CountryField';
import TextField from '@/components/forms/TextField';

export interface AddressFieldsProps {
  prefix: string extends '' ? never : string;
}

const AddressFields: React.FC<AddressFieldsProps> = ({prefix}) => (
  <>
    <TextField
      name={`${prefix}.company`}
      label={<FormattedMessage description="Delivery address: company" defaultMessage="Company" />}
    />
    <TextField
      name={`${prefix}.chamberOfCommerce`}
      label={<FormattedMessage description="Delivery address: kvk" defaultMessage="KVK" />}
    />
    <TextField
      name={`${prefix}.street`}
      label={<FormattedMessage description="Delivery address: street" defaultMessage="Street" />}
      required
    />
    <TextField
      name={`${prefix}.number`}
      label={<FormattedMessage description="Delivery address: number" defaultMessage="Number" />}
      required
    />
    <TextField
      name={`${prefix}.city`}
      label={<FormattedMessage description="Delivery address: city" defaultMessage="City" />}
      required
    />
    <TextField
      name={`${prefix}.postalCode`}
      label={<FormattedMessage description="Delivery address: zip" defaultMessage="ZIP code" />}
      required
    />
    <CountryField
      name={`${prefix}.country`}
      label={<FormattedMessage description="Checkout address: country" defaultMessage="Country" />}
      required
      placeholder={
        <FormattedMessage
          description="Country dropdown placeholder"
          defaultMessage="Select country"
        />
      }
    />
  </>
);

export default AddressFields;

import TextField from '@/forms/TextField';
import {FormattedMessage} from 'react-intl';

import {Customer} from './types';

export interface PersonalDetailsFieldsProps {
  customer: Customer;
}

const PersonalDetailsFields: React.FC<PersonalDetailsFieldsProps> = ({customer}) => (
  <>
    <div className="row">
      <TextField
        name="customer.firstName"
        label={
          <FormattedMessage description="Checkout address: firstName" defaultMessage="First name" />
        }
        autoFocus={!customer.firstName}
        required
        formGroupProps={{className: 'col-md-6 col-xs-12'}}
      />

      <TextField
        name="customer.lastName"
        label={
          <FormattedMessage description="Checkout address: lastName" defaultMessage="Last name" />
        }
        required
        formGroupProps={{className: 'col-md-6 col-xs-12'}}
      />
    </div>

    <TextField
      name={`customer.email`}
      label={
        <FormattedMessage description="Checkout address: email" defaultMessage="Email address" />
      }
      required
    />

    <TextField
      name={`customer.phone`}
      label={
        <FormattedMessage description="Checkout address: phone" defaultMessage="Phone number" />
      }
    />
  </>
);

export default PersonalDetailsFields;

import {useFormikContext} from 'formik';
import {FormattedMessage, FormattedNumber, useIntl} from 'react-intl';

import {getCountryName} from '@/components/forms/CountryField';

import {useCheckoutContext} from './Context';
import type {FormikValues} from './Delivery';

const ShippingCosts: React.FC = () => {
  const intl = useIntl();
  const {shippingCosts} = useCheckoutContext();
  const {
    values: {deliveryMethod, deliveryAddress},
  } = useFormikContext<FormikValues>();
  const country = deliveryAddress?.country;
  if (deliveryMethod !== 'mail' || !country) {
    return null;
  }

  const {weight, price} = shippingCosts;
  return (
    <FormattedMessage
      tagName="p"
      description="Shipping costs value"
      defaultMessage="Shipping to {country} ({weight}): {price}"
      values={{
        country: getCountryName(intl, country),
        weight,
        price: <FormattedNumber value={price} style="currency" currency="EUR" />,
      }}
    />
  );
};

export default ShippingCosts;

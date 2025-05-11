import {useFormikContext} from 'formik';
import {FormattedMessage, FormattedNumber, useIntl} from 'react-intl';
import useAsync from 'react-use/esm/useAsync';

import {getCountryName} from '@/components/forms/CountryField';
import {calculateShippingCosts} from '@/data/shop/payment';

import {useCheckoutContext} from './Context';
import type {FormikValues} from './Delivery';

const ShippingCosts: React.FC = () => {
  const intl = useIntl();
  const {cartId, shippingCosts, onChangeShippingCosts} = useCheckoutContext();
  const {
    values: {deliveryMethod, deliveryAddress},
  } = useFormikContext<FormikValues>();
  const country = deliveryAddress?.country;

  const {loading, error} = useAsync(async () => {
    if (!cartId || !country) return undefined;

    if (deliveryMethod === 'pickup') {
      onChangeShippingCosts({price: 0, weight: ''});
      return;
    } else {
      const info = await calculateShippingCosts(cartId, country);
      onChangeShippingCosts(info);
    }
  }, [onChangeShippingCosts, cartId, deliveryMethod, country]);

  if (error) throw error;

  if (deliveryMethod !== 'mail' || !country || loading) {
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

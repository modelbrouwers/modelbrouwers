import {useFormikContext} from 'formik';
import {FormattedMessage, FormattedNumber, useIntl} from 'react-intl';
import useAsync from 'react-use/esm/useAsync';

import {getCountryName} from '@/components/forms/CountryField';
import {calculateShippingCosts} from '@/data/shop/payment';

import type {FormikValues} from './Delivery';

type CountryValue = NonNullable<FormikValues['deliveryAddress']>['country'];

interface ShippingCostsInfo {
  price: number;
  weight: string;
}

const fetchShippingCosts = async (
  cartId: number,
  country: CountryValue,
): Promise<ShippingCostsInfo> => {
  const {weight, price: priceStr} = await calculateShippingCosts(cartId, country);
  return {
    price: parseFloat(priceStr),
    weight,
  };
};

export interface ShippingCostsProps {
  cartId: number;
}

const ShippingCosts: React.FC<ShippingCostsProps> = ({cartId}) => {
  const intl = useIntl();
  const {
    values: {deliveryMethod, deliveryAddress},
  } = useFormikContext<FormikValues>();
  const country = deliveryAddress?.country;

  const {
    loading,
    error,
    value: costInfo,
  } = useAsync(async () => {
    if (!cartId || !country) return undefined;

    if (deliveryMethod === 'pickup') {
      // cartStore.setShippingCosts(0);
      return undefined;
    }

    const info = await fetchShippingCosts(cartId, country);
    // cartStore.setShippingCosts(info.price);
    return info;
  }, [cartId, country, deliveryMethod]);

  if (error) throw error;

  if (deliveryMethod !== 'mail' || !country || loading || !costInfo) {
    return null;
  }

  const {weight, price} = costInfo;
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

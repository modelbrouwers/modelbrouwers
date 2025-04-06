import { FormattedMessage, FormattedNumber, useIntl } from "react-intl";
import { useFormikContext } from "formik";

import { getCountryName } from "@/components/forms/CountryField";
import type { CartStore } from "@/shop/store";

import type { FormikValues } from "./Address";
import { PaymentConsumer } from "@/data/shop/payment.js";
import useAsync from "react-use/esm/useAsync";

const paymentConsumer = new PaymentConsumer();

type CountryValue =
  | undefined
  | NonNullable<FormikValues["deliveryAddress"]>["country"];

interface ShippingCostsInfo {
  price: number;
  weight: string;
}

const fetchShippingCosts = async (
  cartId: number,
  country: CountryValue,
): Promise<ShippingCostsInfo> => {
  const { weight, price: priceStr } =
    await paymentConsumer.calculateShippingCosts(cartId, country);
  return {
    price: parseFloat(priceStr),
    weight,
  };
};

export interface ShippingCostsProps {
  cartStore: CartStore;
}

const ShippingCosts: React.FC<ShippingCostsProps> = ({ cartStore }) => {
  const intl = useIntl();
  const {
    values: { deliveryMethod, deliveryAddress },
  } = useFormikContext<FormikValues>();
  const country = deliveryAddress?.country;
  const { id: cartId } = cartStore;

  const {
    loading,
    error,
    value: costInfo,
  } = useAsync(async () => {
    if (!cartId || !country) return undefined;

    if (deliveryMethod === "pickup") {
      cartStore.setShippingCosts(0);
      return undefined;
    }

    const info = await fetchShippingCosts(cartId, country);
    cartStore.setShippingCosts(info.price);
    return info;
  }, [cartStore, cartId, country, deliveryMethod]);

  if (error) throw error;

  if (deliveryMethod !== "mail" || !country || loading || !costInfo) {
    return null;
  }

  const { weight, price } = costInfo;
  return (
    <FormattedMessage
      tagName="p"
      description="Shipping costs value"
      defaultMessage="Shipping to {country} ({weight}): {price}"
      values={{
        country: getCountryName(intl, country),
        weight,
        price: (
          <FormattedNumber value={price} style="currency" currency="EUR" />
        ),
      }}
    />
  );
};

export default ShippingCosts;

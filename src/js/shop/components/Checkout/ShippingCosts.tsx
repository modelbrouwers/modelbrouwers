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
  onPriceRetrieved?: (price: number) => void;
}

const ShippingCosts: React.FC<ShippingCostsProps> = ({
  cartStore: { id: cartId },
  onPriceRetrieved,
}) => {
  const intl = useIntl();
  const {
    values: { deliveryMethod, deliveryAddress },
  } = useFormikContext<FormikValues>();
  const country = deliveryAddress?.country;

  const {
    loading,
    error,
    value: costInfo,
  } = useAsync(async () => {
    if (deliveryMethod === "pickup" || !cartId) return undefined;
    const info = await fetchShippingCosts(cartId, country);
    onPriceRetrieved?.(info.price);
    return info;
  }, [cartId, country, deliveryMethod]);

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

import { useFormikContext } from "formik";
import type { FormikValues } from "./Address";
import {
  FormattedMessage,
  MessageDescriptor,
  defineMessage,
  useIntl,
} from "react-intl";
import Select from "@/components/forms/Select";
import { useEffect } from "react";

export interface DeliveryMethodProps {}

interface OptionDescription {
  value: FormikValues["deliveryMethod"];
  label: MessageDescriptor;
}

interface DeliveryMethodOption {
  value: FormikValues["deliveryMethod"];
  label: string;
}

const DELIVERY_OPTIONS: OptionDescription[] = [
  {
    value: "mail",
    label: defineMessage({
      description: "Delivery method 'mail' option label",
      defaultMessage: "By mail",
    }),
  },
  {
    value: "pickup",
    label: defineMessage({
      description: "Delivery method 'mail' option label",
      defaultMessage: "Pickup",
    }),
  },
];

const DeliveryMethod: React.FC<DeliveryMethodProps> = ({}) => {
  const intl = useIntl();
  const {
    values: { deliveryMethod },
    setFieldValue,
  } = useFormikContext<FormikValues>();

  useEffect(() => {
    if (deliveryMethod === "pickup") {
      setFieldValue("deliveryAddress", null);
      setFieldValue("billingAddress", null);
      setFieldValue("billingSameAsDelivery", true);
    }
  }, [deliveryMethod]);

  const deliveryOptions = DELIVERY_OPTIONS.map(({ value, label }) => ({
    value,
    label: intl.formatMessage(label),
  }));

  return (
    <Select<DeliveryMethodOption>
      name="deliveryMethod"
      label={
        <FormattedMessage
          description="Delivery method form field label"
          defaultMessage="Delivery method"
        />
      }
      options={deliveryOptions}
      required
    />
  );
};

export default DeliveryMethod;

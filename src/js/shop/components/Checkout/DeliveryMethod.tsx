import {useFormikContext} from 'formik';
import {useEffect, useState} from 'react';
import {FormattedMessage, MessageDescriptor, defineMessage, useIntl} from 'react-intl';

import Select from '@/components/forms/Select';

import type {FormikValues} from './Address';

interface OptionDescription {
  value: FormikValues['deliveryMethod'];
  label: MessageDescriptor;
}

interface DeliveryMethodOption {
  value: FormikValues['deliveryMethod'];
  label: string;
}

const DELIVERY_OPTIONS: OptionDescription[] = [
  {
    value: 'mail',
    label: defineMessage({
      description: "Delivery method 'mail' option label",
      defaultMessage: 'By mail',
    }),
  },
  {
    value: 'pickup',
    label: defineMessage({
      description: "Delivery method 'mail' option label",
      defaultMessage: 'Pickup',
    }),
  },
];

const DeliveryMethod: React.FC = () => {
  const intl = useIntl();
  const {
    values: {deliveryMethod, deliveryAddress, billingSameAsDelivery, billingAddress},
    setFieldValue,
  } = useFormikContext<FormikValues>();
  const [previousAddressFields, setPreviousAddressFields] =
    useState<Pick<FormikValues, 'deliveryAddress' | 'billingSameAsDelivery' | 'billingAddress'>>();

  useEffect(() => {
    if (deliveryMethod === 'pickup') {
      setPreviousAddressFields({
        deliveryAddress,
        billingSameAsDelivery,
        billingAddress,
      });
      setFieldValue('deliveryAddress', null);
      setFieldValue('billingSameAsDelivery', true);
      setFieldValue('billingAddress', null);
    } else if (deliveryMethod === 'mail' && previousAddressFields) {
      const {deliveryAddress, billingSameAsDelivery, billingAddress} = previousAddressFields;
      setFieldValue('deliveryAddress', deliveryAddress);
      setFieldValue('billingSameAsDelivery', billingSameAsDelivery);
      setFieldValue('billingAddress', billingAddress);
    }
  }, [deliveryMethod]);

  const deliveryOptions = DELIVERY_OPTIONS.map(({value, label}) => ({
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

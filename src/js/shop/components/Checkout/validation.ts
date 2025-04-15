import {IntlShape, defineMessage} from 'react-intl';

import {Address, AddressDetails, Customer} from './types';

const ERR_REQUIRED = defineMessage({
  description: 'Validation error message for required field',
  defaultMessage: 'This field is required.', // TODO: add labels
});

type Errors<T extends object> = {
  [K in keyof T]?: string | (T[K] extends object ? Errors<T[K]> : string);
};

function makeMandatoryFieldsValidator<T extends object>(fields: Array<keyof T>) {
  function validator(obj: Partial<T>, intl: IntlShape): Errors<T> {
    const errors: Errors<T> = {};
    for (const fieldName of fields) {
      if (obj[fieldName]) continue;
      errors[fieldName] = intl.formatMessage(ERR_REQUIRED);
    }
    return errors;
  }
  return validator;
}

export const validateAddress = makeMandatoryFieldsValidator<Address>([
  'street',
  'number',
  'city',
  'postalCode',
  'country',
]);

export const validateCustomer = makeMandatoryFieldsValidator<Customer>([
  'firstName',
  'lastName',
  'email',
]);

export const validateAddressDetails = (
  details: Partial<AddressDetails>,
  intl: IntlShape,
): Errors<AddressDetails> => {
  const errors: Errors<AddressDetails> = {};

  const {customer, deliveryAddress, billingAddress} = details;

  if (customer) {
    const customerErrors = validateCustomer(customer, intl);
    if (Object.keys(customerErrors).length) {
      errors.customer = customerErrors;
    }
  }

  if (deliveryAddress) {
    const deliveryAddressErrors = validateAddress(deliveryAddress, intl);
    if (Object.keys(deliveryAddressErrors).length) {
      errors.deliveryAddress = deliveryAddressErrors;
    }
  }

  if (billingAddress) {
    const billingAddressErrors = validateAddress(billingAddress, intl);
    if (Object.keys(billingAddressErrors).length) {
      // @ts-expect-error -> use zod instead to fix the type errors
      errors.billingAddress = billingAddressErrors;
    }
  }

  return errors;
};

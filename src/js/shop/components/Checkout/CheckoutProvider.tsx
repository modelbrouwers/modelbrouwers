import type {FormikErrors} from 'formik';
import {useCallback} from 'react';
import {type ImmerReducer, useImmerReducer} from 'use-immer';

import {CartProduct} from '@/shop/data';

import {CheckoutContext} from './Context';
import type {
  Address,
  AddressValidationErrors,
  CheckoutValidationErrors,
  DeliveryDetails,
  OrderDetails,
  PaymentDetails,
  UserData,
} from './types';

type CheckoutState = DeliveryDetails & PaymentDetails;

type DispatchAction = {
  type: 'SET_DELIVERY_DETAILS';
  payload: DeliveryDetails;
};

const reducer: ImmerReducer<CheckoutState, DispatchAction> = (
  draft: CheckoutState,
  action: DispatchAction,
) => {
  const {type} = action;
  switch (type) {
    case 'SET_DELIVERY_DETAILS': {
      Object.assign(draft, action.payload);
      break;
    }
    default: {
      const exhaustiveCheck: never = type;
      throw new Error(`Unexpected action type ${exhaustiveCheck}`);
    }
  }
};

export interface CheckoutProviderProps {
  user: UserData | null;
  cartId: number;
  cartProducts: CartProduct[];
  onChangeProductAmount: (cartProductId: number, newAmount: number) => Promise<void>;
  initialData: CheckoutState;
  confirmPath: string;
  orderDetails: OrderDetails;
  validationErrors: CheckoutValidationErrors | null;
  children?: React.ReactNode;
}

const CheckoutProvider: React.FC<CheckoutProviderProps> = ({
  user,
  cartId,
  cartProducts,
  onChangeProductAmount,
  initialData,
  confirmPath,
  orderDetails,
  validationErrors,
  children,
}) => {
  const [state, dispatch] = useImmerReducer<CheckoutState, DispatchAction>(reducer, initialData);

  const setDeliveryDetails = useCallback(
    (values: DeliveryDetails) => {
      dispatch({type: 'SET_DELIVERY_DETAILS', payload: values});
    },
    [dispatch],
  );

  const deliveryDetailsErrors: FormikErrors<DeliveryDetails> = {
    customer: {
      firstName: validationErrors?.first_name?.join('\n'),
      lastName: validationErrors?.last_name?.join('\n'),
      email: validationErrors?.email?.join('\n'),
      phone: validationErrors?.phone?.join('\n'),
    },
    deliveryAddress: processAddressValidationErrors(validationErrors?.delivery_address),
    // @ts-expect-error -> the type can't handle the null union.
    billingAddress: processAddressValidationErrors(validationErrors?.invoice_address),
  };
  const hasDeliveryAddressErrors = [
    typeof deliveryDetailsErrors.deliveryAddress === 'string' &&
      deliveryDetailsErrors.deliveryAddress,
    typeof deliveryDetailsErrors.deliveryAddress === 'object' &&
      Object.values(deliveryDetailsErrors.deliveryAddress).some(Boolean),
  ].some(Boolean);
  const hasBillingAddressErrors = [
    typeof deliveryDetailsErrors.billingAddress === 'string' &&
      deliveryDetailsErrors.billingAddress,
    typeof deliveryDetailsErrors.billingAddress === 'object' &&
      Object.values(deliveryDetailsErrors.billingAddress).some(Boolean),
  ].some(Boolean);
  const hasDeliveryDetailsErrors = [
    deliveryDetailsErrors.customer?.firstName,
    deliveryDetailsErrors.customer?.lastName,
    deliveryDetailsErrors.customer?.email,
    deliveryDetailsErrors.customer?.phone,
    hasDeliveryAddressErrors,
    hasBillingAddressErrors,
  ].some(Boolean);

  const paymentErrors: FormikErrors<PaymentDetails> = {
    paymentMethod: validationErrors?.payment_method?.join('\n'),
    // paymentMethodOptions: validationErrors?.payment_method_options,
    // cart: validationErrors?.cart?.join('\n'),
  };
  const hasPaymentErrors = [
    paymentErrors.paymentMethod,
    typeof paymentErrors.paymentMethodOptions === 'string' && paymentErrors.paymentMethodOptions,
    typeof paymentErrors.paymentMethodOptions === 'object' &&
      Object.values(paymentErrors.paymentMethodOptions).some(Boolean),
    validationErrors?.cart?.some(Boolean),
  ].some(Boolean);

  return (
    <CheckoutContext.Provider
      value={{
        isAuthenticated: user !== null,
        cartId,
        cartProducts,
        onChangeProductAmount,
        deliveryDetails: state,
        confirmPath,
        setDeliveryDetails,
        orderDetails,
        validationErrors,
        deliveryDetailsErrors,
        hasDeliveryDetailsErrors,
        paymentErrors,
        hasPaymentErrors,
      }}
    >
      {children}
    </CheckoutContext.Provider>
  );
};

const processAddressValidationErrors = (
  errors: AddressValidationErrors | string[] | undefined,
): FormikErrors<Address> | string | undefined => {
  if (errors === undefined) return undefined;
  if (Array.isArray(errors)) return errors.join('\n');
  return {
    street: errors?.street?.join('\n'),
    number: errors?.number?.join('\n'),
    city: errors?.city?.join('\n'),
    postalCode: errors?.postal_code?.join('\n'),
    country: errors?.country?.join('\n'),
    company: errors?.company?.join('\n'),
    chamberOfCommerce: errors?.chamber_of_commerce?.join('\n'),
  };
};

export default CheckoutProvider;

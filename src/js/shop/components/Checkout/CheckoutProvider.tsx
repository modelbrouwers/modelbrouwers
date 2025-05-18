import type {FormikErrors} from 'formik';
import {useCallback} from 'react';
import {type ImmerReducer, useImmerReducer} from 'use-immer';

import {CartProduct} from '@/shop/data';

import {CheckoutContext} from './Context';
import {type FormikValues as DeliveryValues, LOCAL_STORAGE_KEY} from './Delivery';
import type {
  Address,
  AddressValidationErrors,
  CheckoutValidationErrors,
  ConfirmOrderData,
  DeliveryDetails,
  OrderDetails,
  PaymentDetails,
  ShippingCosts,
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
  shippingCosts: ShippingCosts;
  onChangeShippingCosts: (costs: ShippingCosts) => void;
  checkoutData?: ConfirmOrderData | null;
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
  shippingCosts,
  onChangeShippingCosts,
  checkoutData,
  confirmPath,
  orderDetails,
  validationErrors,
  children,
}) => {
  const initialData: CheckoutState = propsToInitialData(user, checkoutData);
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
        shippingCosts,
        onChangeShippingCosts,
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

const propsToInitialData = (
  user: UserData | null,
  checkoutData: ConfirmOrderData | undefined | null,
): CheckoutState => {
  const localStorageData: string | null = window.localStorage.getItem(LOCAL_STORAGE_KEY);
  const storedDetails: DeliveryValues | null = localStorageData
    ? JSON.parse(localStorageData)
    : null;

  const deliveryMethod = checkoutData?.delivery_method || storedDetails?.deliveryMethod || 'mail';
  const base: Omit<CheckoutState, 'deliveryMethod' | 'deliveryAddress' | 'billingAddress'> = {
    customer: {
      firstName:
        checkoutData?.first_name ?? storedDetails?.customer?.firstName ?? user?.first_name ?? '',
      lastName:
        checkoutData?.last_name ?? storedDetails?.customer?.lastName ?? user?.last_name ?? '',
      email: checkoutData?.email ?? storedDetails?.customer?.email ?? user?.email ?? '',
      phone: checkoutData?.phone ?? storedDetails?.customer?.phone ?? user?.phone ?? '',
    },
    paymentMethod: checkoutData?.payment_method ?? 0,
    paymentMethodOptions: checkoutData?.payment_method_options ?? null,
  };
  if (deliveryMethod === 'pickup') {
    return {...base, deliveryMethod, deliveryAddress: null, billingAddress: null};
  }

  // France is not supported
  const userCountry = user?.profile?.country === 'F' ? 'N' : user?.profile?.country || 'N';

  const addressDefaults: Address = {
    street: '',
    number: '',
    city: '',
    postalCode: '',
    country: userCountry,
    company: '',
    chamberOfCommerce: '',
  };
  const deliveryAddress = checkoutData?.delivery_address
    ? {
        street: checkoutData?.delivery_address?.street,
        number: checkoutData?.delivery_address?.number,
        city: checkoutData?.delivery_address?.city,
        postalCode: checkoutData?.delivery_address?.postal_code,
        country: checkoutData?.delivery_address?.country,
        company: checkoutData?.delivery_address?.company,
        chamberOfCommerce: checkoutData?.delivery_address?.chamber_of_commerce,
      }
    : {
        street: storedDetails?.deliveryAddress?.street ?? user?.profile?.street ?? '',
        number: storedDetails?.deliveryAddress?.number ?? user?.profile?.number ?? '',
        city: storedDetails?.deliveryAddress?.city ?? user?.profile?.city ?? '',
        postalCode: storedDetails?.deliveryAddress?.postalCode ?? user?.profile?.postal ?? '',
        country: storedDetails?.deliveryAddress?.country ?? userCountry,
        company: storedDetails?.deliveryAddress?.company ?? '',
        chamberOfCommerce: storedDetails?.deliveryAddress?.chamberOfCommerce ?? '',
      };

  const billingAddress = checkoutData?.invoice_address
    ? {
        street: checkoutData?.invoice_address?.street,
        number: checkoutData?.invoice_address?.number,
        city: checkoutData?.invoice_address?.city,
        postalCode: checkoutData?.invoice_address?.postal_code,
        country: checkoutData?.invoice_address?.country,
        company: checkoutData?.invoice_address?.company,
        chamberOfCommerce: checkoutData?.invoice_address?.chamber_of_commerce,
      }
    : storedDetails?.billingAddress
      ? {
          ...addressDefaults,
          ...storedDetails?.billingAddress,
        }
      : null;

  return {...base, deliveryMethod, deliveryAddress, billingAddress};
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

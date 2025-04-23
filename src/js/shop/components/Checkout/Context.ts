import {FormikErrors} from 'formik';
import React, {useContext} from 'react';

import {CartProduct} from '@/shop/data';

import type {
  CheckoutValidationErrors,
  DeliveryDetails,
  OrderDetails,
  PaymentDetails,
} from './types';

interface CheckoutContextType {
  isAuthenticated: boolean;
  cartId: number;
  cartProducts: CartProduct[];
  onChangeProductAmount: (cartProductId: number, newAmount: number) => Promise<void>;
  deliveryDetails: DeliveryDetails & PaymentDetails;
  confirmPath: string;
  setDeliveryDetails: (values: DeliveryDetails) => void;
  orderDetails: OrderDetails;
  validationErrors: CheckoutValidationErrors | null;
  deliveryDetailsErrors: FormikErrors<DeliveryDetails>;
  hasDeliveryDetailsErrors: boolean;
  paymentErrors: FormikErrors<PaymentDetails>;
  hasPaymentErrors: boolean;
}

const CheckoutContext = React.createContext<CheckoutContextType>({
  isAuthenticated: false,
  cartId: 0,
  cartProducts: [],
  onChangeProductAmount: async () => {},
  deliveryDetails: {
    customer: {
      firstName: '',
      lastName: '',
      email: '',
      phone: '',
    },
    deliveryMethod: 'pickup',
    deliveryAddress: null,
    billingAddress: null,
    paymentMethod: 0,
    paymentMethodOptions: null,
  },
  confirmPath: '/checkout/confirm/',
  setDeliveryDetails: () => {},
  orderDetails: null,
  validationErrors: null,
  deliveryDetailsErrors: {},
  hasDeliveryDetailsErrors: false,
  paymentErrors: {},
  hasPaymentErrors: false,
});

CheckoutContext.displayName = 'CheckoutContext';

const useCheckoutContext = () => useContext(CheckoutContext);

export {CheckoutContext, useCheckoutContext};

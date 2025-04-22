import React, {useContext} from 'react';

import {CartProduct} from '@/shop/data';

import type {DeliveryDetails, OrderDetails, PaymentDetails} from './types';

interface CheckoutContextType {
  isAuthenticated: boolean;
  cartId: number;
  cartProducts: CartProduct[];
  onChangeProductAmount: (cartProductId: number, newAmount: number) => Promise<void>;
  deliveryDetails: DeliveryDetails & PaymentDetails;
  confirmPath: string;
  setDeliveryDetails: (values: DeliveryDetails) => void;
  orderDetails: OrderDetails;
  // TODO -> recursive structure where every node can be an error list from DRF
  validationErrors: unknown;
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
});

CheckoutContext.displayName = 'CheckoutContext';

const useCheckoutContext = () => useContext(CheckoutContext);

export {CheckoutContext, useCheckoutContext};

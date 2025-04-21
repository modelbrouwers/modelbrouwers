import React, {useContext} from 'react';

import {CartProduct} from '@/shop/data';

import {DeliveryDetails} from './types';

interface CheckoutContextType {
  cartId: number;
  cartProducts: CartProduct[];
  deliveryDetails: DeliveryDetails & {
    paymentMethod: number;
    paymentMethodOptions: null | Record<string, any>;
  };
  confirmPath: string;
  setDeliveryDetails: (values: DeliveryDetails) => void;
  // TODO -> recursive structure where every node can be an error list from DRF
  validationErrors: unknown;
}

const CheckoutContext = React.createContext<CheckoutContextType>({
  cartId: 0,
  cartProducts: [],
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
  validationErrors: null,
});

CheckoutContext.displayName = 'CheckoutContext';

const useCheckoutContext = () => useContext(CheckoutContext);

export {CheckoutContext, useCheckoutContext};

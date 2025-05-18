import {Decorator} from '@storybook/react';
import {fn} from '@storybook/test';
import {useEffect} from 'react';

import {CartProduct} from '@/shop/data';

import CheckoutProvider from './CheckoutProvider';
import {LOCAL_STORAGE_KEY} from './Delivery';

const DEFAULT_CART_PRODUCTS: CartProduct[] = [
  new CartProduct({
    id: 1,
    product: {
      id: 1,
      name: 'Product 1',
      image: 'https://loremflickr.com/400/300/cat',
      price: 3.78,
      model_name: 'MB01',
    },
    amount: 1,
  }),
  new CartProduct({
    id: 2,
    product: {
      id: 2,
      name: 'Product 2',
      image: 'https://loremflickr.com/400/300/cat',
      price: 2.07,
      model_name: 'MB02',
    },
    amount: 3,
  }),
];

const clearLocalStorage = () => {
  window.localStorage.removeItem(LOCAL_STORAGE_KEY);
};

export const withCheckout: Decorator = (Story, {parameters}) => {
  // ensure we clear items from the local storage before and after to clean up side
  // effects
  useEffect(() => {
    clearLocalStorage();
    return clearLocalStorage;
  }, []);

  const checkoutParams = parameters?.checkout;
  const checkoutData = checkoutParams?.checkoutData;
  return (
    <CheckoutProvider
      user={checkoutParams?.user ?? null}
      cartId={checkoutParams?.cartId ?? 12}
      cartProducts={checkoutParams?.cartProducts ?? DEFAULT_CART_PRODUCTS}
      onChangeProductAmount={checkoutParams?.onChangeProductAmount ?? fn()}
      shippingCosts={checkoutParams?.shippingCosts ?? {price: 0, weight: ''}}
      onChangeShippingCosts={checkoutParams?.onChangeShippingCosts ?? fn()}
      checkoutData={checkoutData}
      confirmPath="/winkel/checkout/confirm"
      orderDetails={checkoutParams?.orderDetails ?? null}
      validationErrors={checkoutParams?.validationErrors ?? null}
    >
      <Story />
    </CheckoutProvider>
  );
};

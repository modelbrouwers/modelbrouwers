import {Decorator} from '@storybook/react';
import {fn} from '@storybook/test';

import {CartProduct} from '@/shop/data';

import CheckoutProvider, {CheckoutProviderProps} from './CheckoutProvider';

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

const DEFAULT_INITIAL_DATA: CheckoutProviderProps['initialData'] = {
  deliveryMethod: 'mail',
  deliveryAddress: {
    country: 'N',
    street: '',
    number: '',
    city: '',
    postalCode: '',
    company: '',
    chamberOfCommerce: '',
  },
  billingAddress: null,
  customer: {
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
  },
  paymentMethod: 0,
  paymentMethodOptions: null,
};

export const withCheckout: Decorator = (Story, {parameters}) => {
  const checkoutParams = parameters?.checkout;
  const initialData = {...DEFAULT_INITIAL_DATA, ...(checkoutParams?.initialData ?? {})};
  return (
    <CheckoutProvider
      user={checkoutParams?.user ?? null}
      cartId={checkoutParams?.cartId ?? 12}
      cartProducts={checkoutParams?.cartProducts ?? DEFAULT_CART_PRODUCTS}
      onChangeProductAmount={checkoutParams?.onChangeProductAmount ?? fn()}
      initialData={initialData}
      confirmPath="/winkel/checkout/confirm"
      orderDetails={checkoutParams?.orderDetails ?? null}
      validationErrors={checkoutParams?.validationErrors ?? null}
    >
      <Story />
    </CheckoutProvider>
  );
};

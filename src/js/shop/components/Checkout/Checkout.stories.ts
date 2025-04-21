import type {Meta, StoryObj} from '@storybook/react';
import {fn} from '@storybook/test';
import {reactRouterParameters, withRouter} from 'storybook-addon-remix-react-router';

import {CartProduct} from '@/shop/data';

import Checkout from './Checkout';

export default {
  title: 'Shop / Checkout / Flow',
  component: Checkout,
  decorators: [withRouter],
  args: {
    cartId: 42,
    user: {},
    cartProducts: [
      new CartProduct({
        id: 1,
        product: {
          id: 42,
          name: 'Polish set',
          image: 'https://loremflickr.com/100/100/cat',
          model_name: 'XYZ-001',
          price: 9.99,
        },
        amount: 1,
      }),
    ],
    onChangeAmount: fn(),
    confirmPath: '/winkel/checkout/confirm/',
    checkoutData: {},
    orderDetails: null,
    validationErrors: {},
  },
  parameters: {
    reactRouter: reactRouterParameters({
      routing: {path: '/'},
    }),
  },
} satisfies Meta<typeof Checkout>;

type Story = StoryObj<typeof Checkout>;

export const Account: Story = {};

import type {Meta, StoryObj} from '@storybook/react';
import {fn} from '@storybook/test';

import {CartProduct} from '@/shop/data';

import CartDetail from './CartDetail';

export default {
  title: 'Shop / Cart / CartDetail',
  component: CartDetail,
  args: {
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
      new CartProduct({
        id: 2,
        product: {
          id: 43,
          name: 'Rubber gloves',
          image: 'https://loremflickr.com/100/100/cat',
          model_name: 'MB-999',
          price: 0.5,
        },
        amount: 5,
      }),
    ],
    onChangeAmount: fn(),
    checkoutPath: '/winkel/checkout/',
    indexPath: '/winkel/',
  },
} satisfies Meta<typeof CartDetail>;

type Story = StoryObj<typeof CartDetail>;

export const Default: Story = {};

export const WithShippingCosts: Story = {
  args: {
    shippingCosts: 2.99,
  },
};

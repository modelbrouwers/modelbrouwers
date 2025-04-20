import type {Meta, StoryObj} from '@storybook/react';
import {fn, userEvent, within} from '@storybook/test';

import {CartProduct} from '@/shop/data';

import TopbarCart from './TopbarCart';

export default {
  title: 'Shop / Cart / TopbarCart',
  component: TopbarCart,
  args: {
    cartProducts: [
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
    ],
    checkoutPath: '/winkel/checkout/',
    cartDetailPath: '/winkel/cart/123/',
    onRemoveProduct: fn(),
  },
  parameters: {
    layout: 'centered',
  },
} satisfies Meta<typeof TopbarCart>;

type Story = StoryObj<typeof TopbarCart>;

export const Default: Story = {
  name: 'TopbarCart',
  play: async ({canvasElement}) => {
    const canvas = within(canvasElement);
    await userEvent.hover(canvas.getByText('4 items'));
  },
};

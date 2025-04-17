import type {Meta, StoryObj} from '@storybook/react';
import {userEvent, within} from '@storybook/test';

import TopbarCart from './TopbarCart';

export default {
  title: 'Shop / Cart / TopbarCart',
  component: TopbarCart,
  args: {
    checkoutPath: '/winkel/checkout/',
    cartDetailPath: '/winkel/cart/123/',
    store: {
      amount: 2,
      products: [
        {
          id: 1,
          product: {
            name: 'Product 1',
            image: 'https://loremflickr.com/400/300/cat',
          },
          amount: 1,
          totalStr: (2.78).toFixed(2),
        },
        {
          id: 2,
          product: {
            name: 'Product 2',
            image: 'https://loremflickr.com/400/300/cat',
          },
          amount: 3,
          totalStr: (7.21).toFixed(2),
        },
      ],
      total: (9.99).toFixed(2), // FIXME: properly localize (!)
    },
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
    await userEvent.hover(canvas.getByText('2 items'));
  },
};

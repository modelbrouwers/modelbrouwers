import type {Meta, StoryObj} from '@storybook/react';

import CartDetail from './CartDetail';

export default {
  title: 'Shop / Cart / CartDetail',
  component: CartDetail,
  args: {
    store: {
      products: [
        {
          product: {
            id: 42,
            name: 'Polish set',
            image: 'https://loremflickr.com/100/100/cat',
            model_name: 'XYZ-001',
            price: '9,99',
            totalStr: '9,99',
          },
          amount: 1,
          totalStr: '9,99',
        },
      ],
      user: {},
      id: 42,
      total: '12,99',
    },
    checkoutPath: '/winkel/checkout',
    indexPath: '/winkel',
  },
} satisfies Meta<typeof CartDetail>;

type Story = StoryObj<typeof CartDetail>;

export const Default: Story = {
  name: 'CartDetail',
};

import type {Meta, StoryObj} from '@storybook/react';

import ProductImage from './ProductImage';

export default {
  title: 'Shop / Cart / ProductImage',
  component: ProductImage,
  args: {
    product: {
      id: 1,
      name: 'A product',
      image: 'https://loremflickr.com/400/300/cat',
      price: 0.99,
      model_name: 'EU123',
    },
  },
} satisfies Meta<typeof ProductImage>;

type Story = StoryObj<typeof ProductImage>;

export const Default: Story = {
  name: 'ProductImage',
};

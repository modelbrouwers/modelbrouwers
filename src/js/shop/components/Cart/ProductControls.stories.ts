import type {Meta, StoryObj} from '@storybook/react';
import {fn} from '@storybook/test';

import ProductControls from './ProductControls';

export default {
  title: 'Shop / Cart / ProductControls',
  component: ProductControls,
  args: {
    currentAmount: 1,
    onChangeAmount: fn(),
    hasStock: true,
    onAddProduct: fn(),
  },
  parameters: {
    layout: 'centered',
  },
} satisfies Meta<typeof ProductControls>;

type Story = StoryObj<typeof ProductControls>;

export const Default: Story = {};

export const CannotIncrement: Story = {
  args: {
    hasStock: false,
  },
};

export const ZeroAmountCanAdd: Story = {
  args: {
    currentAmount: 0,
    hasStock: true,
  },
};

export const ZeroAmountCannotAdd: Story = {
  args: {
    currentAmount: 0,
    hasStock: false,
  },
};

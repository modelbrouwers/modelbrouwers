import type {Meta, StoryObj} from '@storybook/react';

import Loader from './Loader';

export default {
  title: 'General purpose / Loader',
  component: Loader,
} satisfies Meta<typeof Loader>;

type Story = StoryObj<typeof Loader>;

export const Default: Story = {};

export const Small: Story = {
  args: {
    size: 2,
  },
};

export const Tiny: Story = {
  args: {
    size: 1,
  },
};

export const Centered: Story = {
  args: {
    center: true,
    size: 4,
  },
};

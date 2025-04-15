import type {Meta, StoryObj} from '@storybook/react';

import Loader from './Loader';

export default {
  title: 'General purpose / Loader',
  component: Loader,
} satisfies Meta<typeof Loader>;

type Story = StoryObj<typeof Loader>;

export const Default: Story = {
  name: 'Loader',
};

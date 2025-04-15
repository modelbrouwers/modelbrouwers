import type {Meta, StoryObj} from '@storybook/react';
import {fn} from '@storybook/test';

import {IncrementButton} from './AmountButtons';

export default {
  title: 'Shop / Cart / IncrementButton',
  component: IncrementButton,
  args: {
    onClick: fn(),
  },
} satisfies Meta<typeof IncrementButton>;

type Story = StoryObj<typeof IncrementButton>;

export const Default: Story = {
  name: 'IncrementButton',
};

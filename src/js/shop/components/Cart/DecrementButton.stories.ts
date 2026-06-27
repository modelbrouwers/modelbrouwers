import type {Meta, StoryObj} from '@storybook/react-webpack5';

import {fn} from 'storybook/test';

import {DecrementButton} from './AmountButtons';

export default {
  title: 'Shop / Cart / DecrementButton',
  component: DecrementButton,
  args: {
    onClick: fn(),
  },
} satisfies Meta<typeof DecrementButton>;

type Story = StoryObj<typeof DecrementButton>;

export const Default: Story = {
  name: 'DecrementButton',
};

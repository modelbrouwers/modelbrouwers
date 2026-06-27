import type {Meta, StoryObj} from '@storybook/react-webpack5';
import {reactRouterParameters, withRouter} from 'storybook-addon-remix-react-router';

import Account from './Account';

export default {
  title: 'Shop / Checkout / Account',
  component: Account,
  decorators: [withRouter],
  args: {
    nextAfterLogin: '/winkel/checkout/',
  },
  parameters: {
    reactRouter: reactRouterParameters({
      routing: {path: '/winkel/checkout/'},
    }),
  },
} satisfies Meta<typeof Account>;

type Story = StoryObj<typeof Account>;

export const Default: Story = {
  name: 'Account',
};

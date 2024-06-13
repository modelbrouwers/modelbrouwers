import type { Meta, StoryObj } from "@storybook/react";
import {
  reactRouterParameters,
  withRouter,
} from "storybook-addon-remix-react-router";

import Account from "./Account";

export default {
  title: "Shop / Checkout / Account",
  component: Account,
  decorators: [withRouter],
  args: {
    isAuthenticated: false,
    currentLocation: "/winkel/checkout/account",
  },
  parameters: {
    reactRouter: reactRouterParameters({
      routing: { path: "/winkel/checkout/account" },
    }),
  },
} satisfies Meta<typeof Account>;

type Story = StoryObj<typeof Account>;

export const Default: Story = {
  name: "Account",
};

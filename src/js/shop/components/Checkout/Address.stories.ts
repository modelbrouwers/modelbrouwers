import type { Meta, StoryObj } from "@storybook/react";
import { fn } from "@storybook/test";
import {
  reactRouterParameters,
  withRouter,
} from "storybook-addon-remix-react-router";

import Address from "./Address";

export default {
  title: "Shop / Checkout / Address / Full page",
  component: Address,
  decorators: [withRouter],
  args: {
    allowSubmit: false,
    customer: {
      firstName: "Arsene",
      lastName: "Lupin",
      email: "arsene@lupin.fr",
      phone: "",
    },
    deliveryAddress: {
      company: "",
      chamberOfCommerce: "",
      street: "Avenue des Champs-Élysées",
      number: "42",
      city: "Paris",
      postalCode: "75008",
      country: "N",
    },
    billingAddress: undefined,
    onSubmit: fn(),
  },
  parameters: {
    reactRouter: reactRouterParameters({
      routing: { path: "/winkel/checkout/address" },
    }),
  },
} satisfies Meta<typeof Address>;

type Story = StoryObj<typeof Address>;

export const Default: Story = { name: "Full page" };

import type { Meta, StoryObj } from "@storybook/react";
import { fn, expect, within, waitFor } from "@storybook/test";
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
    onSubmit: fn(),
  },
  parameters: {
    reactRouter: reactRouterParameters({
      routing: { path: "/winkel/checkout/address" },
    }),
  },
} satisfies Meta<typeof Address>;

type Story = StoryObj<typeof Address>;

export const Empty: Story = {
  args: {
    customer: {
      firstName: "",
      lastName: "",
      email: "",
      phone: "",
    },
    deliveryAddress: {
      company: "",
      chamberOfCommerce: "",
      street: "",
      number: "",
      city: "",
      postalCode: "",
      country: "N",
    },
    billingAddress: null,
  },

  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    await waitFor(() => {
      expect(canvas.getByRole("button", { name: "Continue" })).toBeDisabled();
    });
  },
};

export const BillingAddressSameAsDelivery: Story = {
  args: {
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
    billingAddress: null,
  },

  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    expect(
      canvas.getByLabelText("My billing and delivery address are the same."),
    ).toBeChecked();
    await waitFor(() => {
      expect(
        canvas.getByRole("button", { name: "Continue" }),
      ).not.toBeDisabled();
    });
  },
};

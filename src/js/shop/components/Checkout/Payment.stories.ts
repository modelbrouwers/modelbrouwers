import type { Meta, StoryObj } from "@storybook/react";
import {
  reactRouterParameters,
  withRouter,
} from "storybook-addon-remix-react-router";
import { http, HttpResponse } from "msw";

import { API_ROOT } from "@/constants.js";
import { CartStore } from "@/shop/store";

import Payment from "./Payment";

export default {
  title: "Shop / Checkout / Payment",
  component: Payment,
  decorators: [withRouter],
  args: {
    cartStore: new CartStore({
      id: 123,
      user: {
        username: 'BBT',
        first_name: 'B.',
        last_name: 'BT',
        email: 'bbt@example.com',
        phone: '',
      },
      status: 'open',
      products: [{
          id: 456,
          cart: 123,
          product: {
            id: 42,
            name: "Polish set",
            image: "https://loremflickr.com/100/100/cat",
            model_name: "XYZ-001",
            price: 9.99,
            totalStr: "9,99",
          },
          amount: 1,
          total: '9.99',
        }],
      total: "12,99",
    }),
    csrftoken: "csrftoken",
    confirmPath: "/winkel/checkout/confirm",
    errors: {},
    checkoutDetails: {
      customer: {
        firstName: "Arsene",
        lastName: "Lupin",
        email: "arsene@lupin.fr",
        phone: "",
      },
      deliveryMethod: "mail",
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
  },
  argTypes: {
    cartStore: {table: {disable: true}}
  },
  parameters: {
    reactRouter: reactRouterParameters({
      routing: { path: "/winkel/checkout/payment" },
    }),
    msw: {
      handlers: [
        http.get(`${API_ROOT}api/v1/shop/paymentmethod/`, () => {
          return HttpResponse.json([
            { id: 1, name: "Payment method 1", logo: "", order: 2 },
            { id: 2, name: "Payment method 2", logo: "", order: 3 },
            {
              id: 3,
              name: "iDeal",
              logo: "/assets/ideal-logo-1024.png",
              order: 1,
            },
          ]);
        }),
        http.get(`${API_ROOT}api/v1/shop/ideal_banks/`, () => {
          return HttpResponse.json([
            { id: 1, name: "Bank 1" },
            { id: 2, name: "Bank 2" },
            { id: 3, name: "Bank 3" },
          ]);
        }),
      ],
    },
  },
} satisfies Meta<typeof Payment>;

type Story = StoryObj<typeof Payment>;

export const Default: Story = {
  name: "Payment",
};

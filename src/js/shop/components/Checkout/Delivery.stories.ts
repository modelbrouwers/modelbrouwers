import type {Meta, StoryObj} from '@storybook/react';
import {expect, fn, waitFor, within} from '@storybook/test';
import {HttpResponse, http} from 'msw';
import {reactRouterParameters, withRouter} from 'storybook-addon-remix-react-router';

import {API_ROOT} from '@/constants.js';
import {CartStore} from '@/shop/store.js';

import Delivery from './Delivery';

export default {
  title: 'Shop / Checkout / Delivery / Full page',
  component: Delivery,
  decorators: [withRouter],
  args: {
    onSubmit: fn(),
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
      products: [],
      total: '9,99',
    }),
  },
  argTypes: {
    cartStore: {table: {disable: true}},
  },
  parameters: {
    reactRouter: reactRouterParameters({
      routing: {path: '/winkel/checkout/address'},
    }),
    msw: {
      handlers: [
        http.get(`${API_ROOT}api/v1/shop/shipping-costs/`, () => {
          return HttpResponse.json({
            price: 11.9,
            weight: '320 g',
          });
        }),
      ],
    },
  },
} satisfies Meta<typeof Delivery>;

type Story = StoryObj<typeof Delivery>;

export const Empty: Story = {
  args: {
    customer: {
      firstName: '',
      lastName: '',
      email: '',
      phone: '',
    },
    deliveryAddress: {
      company: '',
      chamberOfCommerce: '',
      street: '',
      number: '',
      city: '',
      postalCode: '',
      country: 'N',
    },
    billingAddress: null,
  },

  play: async ({canvasElement}) => {
    const canvas = within(canvasElement);

    await waitFor(() => {
      expect(canvas.getByRole('button', {name: 'Continue'})).toBeDisabled();
    });
  },
};

export const BillingAddressSameAsDelivery: Story = {
  args: {
    customer: {
      firstName: 'Arsene',
      lastName: 'Lupin',
      email: 'arsene@lupin.fr',
      phone: '',
    },
    deliveryAddress: {
      company: '',
      chamberOfCommerce: '',
      street: 'Avenue des Champs-Élysées',
      number: '42',
      city: 'Paris',
      postalCode: '75008',
      country: 'N',
    },
    billingAddress: null,
  },

  play: async ({canvasElement}) => {
    const canvas = within(canvasElement);

    expect(canvas.getByLabelText('My billing and delivery address are the same.')).toBeChecked();
    await waitFor(() => {
      expect(canvas.getByRole('button', {name: 'Continue'})).not.toBeDisabled();
    });
  },
};

export const DifferentBillingAddress: Story = {
  args: {
    customer: {
      firstName: 'Arsene',
      lastName: 'Lupin',
      email: 'arsene@lupin.fr',
      phone: '',
    },
    deliveryAddress: {
      company: '',
      chamberOfCommerce: '',
      street: 'Avenue des Champs-Élysées',
      number: '42',
      city: 'Paris',
      postalCode: '75008',
      country: 'N',
    },
    billingAddress: {
      company: '',
      chamberOfCommerce: '',
      street: '',
      number: '',
      city: '',
      postalCode: '',
      country: 'N',
    },
  },

  play: async ({canvasElement}) => {
    const canvas = within(canvasElement);

    expect(
      canvas.getByLabelText('My billing and delivery address are the same.'),
    ).not.toBeChecked();
    await waitFor(() => {
      expect(canvas.getByRole('button', {name: 'Continue'})).toBeDisabled();
    });
  },
};

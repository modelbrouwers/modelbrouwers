import type {Meta, StoryObj} from '@storybook/react';
import {expect, fn, waitFor, within} from '@storybook/test';
import {HttpResponse, http} from 'msw';
import {reactRouterParameters, withRouter} from 'storybook-addon-remix-react-router';

import {API_ROOT} from '@/constants.js';

import Delivery from './Delivery';
import {withCheckout} from './storybook';
import type {ConfirmOrderData} from './types';

export default {
  title: 'Shop / Checkout / Delivery / Full page',
  component: Delivery,
  decorators: [withRouter, withCheckout],
  args: {
    onSubmit: fn(),
    cartId: 123,
  },
  parameters: {
    reactRouter: reactRouterParameters({
      routing: {path: '/winkel/checkout/address'},
    }),
    checkout: {
      shippingCosts: {
        price: 11.9,
        weight: '320 g',
      },
    },
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
  play: async ({canvasElement}) => {
    const canvas = within(canvasElement);

    await waitFor(() => {
      expect(canvas.getByRole('button', {name: 'Continue'})).toBeDisabled();
    });
  },
};

export const BillingAddressSameAsDelivery: Story = {
  parameters: {
    checkout: {
      checkoutData: {
        first_name: 'Arsene',
        last_name: 'Lupin',
        email: 'arsene@lupin.fr',
        phone: '',
        delivery_address: {
          company: '',
          chamber_of_commerce: '',
          street: 'Avenue des Champs-Élysées',
          number: '42',
          city: 'Paris',
          postal_code: '75008',
          country: 'N',
        },
        invoice_address: null,
      } satisfies Partial<ConfirmOrderData>,
    },
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
  parameters: {
    checkout: {
      checkoutData: {
        first_name: 'Arsene',
        last_name: 'Lupin',
        email: 'arsene@lupin.fr',
        phone: '',
        delivery_address: {
          company: '',
          chamber_of_commerce: '',
          street: 'Avenue des Champs-Élysées',
          number: '42',
          city: 'Paris',
          postal_code: '75008',
          country: 'N',
        },
        invoice_address: {
          company: '',
          chamber_of_commerce: '',
          street: '',
          number: '',
          city: '',
          postal_code: '',
          country: 'N',
        },
      } satisfies Partial<ConfirmOrderData>,
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

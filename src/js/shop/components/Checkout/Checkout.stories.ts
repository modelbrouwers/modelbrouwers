import type {Meta, StoryObj} from '@storybook/react';
import {expect, fn, userEvent, waitFor, within} from '@storybook/test';
import {HttpResponse, http} from 'msw';
import {withRouter} from 'storybook-addon-remix-react-router';

import {API_ROOT} from '@/constants.js';
import {CartProduct} from '@/shop/data';

import Checkout from './Checkout';
import checkoutRoutes from './routes';
import {withCheckout} from './storybook';

export default {
  title: 'Shop / Checkout / Flow',
  component: Checkout,
  decorators: [withRouter, withCheckout],
  parameters: {
    checkout: {
      cartId: 42,
      user: null,
      cartProducts: [
        new CartProduct({
          id: 1,
          product: {
            id: 42,
            name: 'Polish set',
            image: 'https://loremflickr.com/100/100/cat',
            model_name: 'XYZ-001',
            price: 9.99,
          },
          amount: 1,
        }),
      ],
      onChangeAmount: fn(),
      confirmPath: '/winkel/checkout/confirm/',
      orderDetails: null,
      validationErrors: {},
      shippingCosts: {
        price: 11.9,
        weight: '320 g',
      },
    },
    reactRouter: {
      routing: checkoutRoutes,
    },
    msw: {
      handlers: [
        http.get(`${API_ROOT}api/v1/shop/shipping-costs/`, () => {
          return HttpResponse.json({
            price: 11.9,
            weight: '320 g',
          });
        }),
        http.get(`${API_ROOT}api/v1/shop/paymentmethod/`, () => {
          return HttpResponse.json([
            {id: 1, name: 'Payment method 1', logo: '', order: 2},
            {id: 2, name: 'Payment method 2', logo: '', order: 3},
            {
              id: 3,
              name: 'iDeal',
              logo: '/assets/ideal-logo-1024.png',
              order: 1,
            },
          ]);
        }),
        http.get(`${API_ROOT}api/v1/shop/ideal_banks/`, () => {
          return HttpResponse.json([
            {id: 1, name: 'Bank 1'},
            {id: 2, name: 'Bank 2'},
            {id: 3, name: 'Bank 3'},
          ]);
        }),
      ],
    },
  },
} satisfies Meta<typeof Checkout>;

type Story = StoryObj<typeof Checkout>;

export const Flow: Story = {
  play: async ({canvasElement, step}) => {
    const canvas = within(canvasElement);

    await step('Account', async () => {
      await userEvent.click(await canvas.findByRole('link', {name: 'Continue without signup'}));
    });

    await step('Delivery details', async () => {
      await userEvent.type(await canvas.findByLabelText('First name'), 'Thomas');
      await userEvent.type(canvas.getByLabelText('Last name'), 'Moore');
      await userEvent.type(canvas.getByLabelText('Email address'), 'thomasmoore@example.com');
      await userEvent.type(canvas.getByLabelText('Street'), 'Burlington Road');
      await userEvent.type(canvas.getByLabelText('Number'), '420');
      await userEvent.type(canvas.getByLabelText('ZIP code'), '1234 AB');
      await userEvent.type(canvas.getByLabelText('City'), 'Volendam');
      await userEvent.tab();

      const submitButton = canvas.getByRole('button', {name: 'Continue'});
      submitButton.focus();
      await waitFor(() => {
        expect(submitButton).not.toBeDisabled();
      });

      await userEvent.click(submitButton);
    });

    await step('Payment details', async () => {
      expect(await canvas.findByRole('heading', {name: 'Cart overview'})).toBeVisible();
    });
  },
};

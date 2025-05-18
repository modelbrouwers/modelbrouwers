import type {Meta, StoryObj} from '@storybook/react';
import {fn} from '@storybook/test';
import {HttpResponse, http} from 'msw';
import {reactRouterParameters, withRouter} from 'storybook-addon-remix-react-router';

import {API_ROOT} from '@/constants.js';
import {CartProduct} from '@/shop/data';

import Payment from './Payment';
import {withCheckout} from './storybook';
import type {ConfirmOrderData} from './types';

export default {
  title: 'Shop / Checkout / Payment',
  component: Payment,
  decorators: [withRouter, withCheckout],
  parameters: {
    checkout: {
      cartId: 10,
      cartProducts: [
        new CartProduct({
          id: 456,
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
      onChangeProductAmount: fn(),
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
    reactRouter: reactRouterParameters({
      routing: {path: '/winkel/checkout/payment'},
    }),
    msw: {
      handlers: [
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
} satisfies Meta<typeof Payment>;

type Story = StoryObj<typeof Payment>;

export const Default: Story = {
  name: 'Payment',
};

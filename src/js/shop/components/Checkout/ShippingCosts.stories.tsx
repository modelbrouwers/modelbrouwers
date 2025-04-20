import type {Meta, StoryObj} from '@storybook/react';
import {useFormikContext} from 'formik';
import {HttpResponse, http} from 'msw';
import {useEffect} from 'react';

import {API_ROOT} from '@/constants.js';
import {CartStore} from '@/shop/store.js';
import {withFormik} from '@/storybook/decorators';

import type {FormikValues} from './Delivery';
import ShippingCosts, {ShippingCostsProps} from './ShippingCosts';

interface Args extends ShippingCostsProps {
  country: NonNullable<FormikValues['deliveryAddress']>['country'];
}

const Wrapper: React.FC<Args> = ({country, ...props}) => {
  const {setFieldValue} = useFormikContext<FormikValues>();
  useEffect(() => {
    setFieldValue('deliveryAddress.country', country);
  }, [country]);
  return <ShippingCosts {...props} />;
};

export default {
  title: 'Shop / Checkout / Delivery / ShippingCosts',
  component: ShippingCosts,
  render: ({...args}) => <Wrapper {...args} />,
  decorators: [withFormik],
  args: {
    country: 'N',
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
    country: {
      control: 'inline-radio',
      options: ['N', 'B', 'D'],
    },
    cartStore: {table: {disable: true}},
  },
  parameters: {
    formik: {
      initialValues: {
        customer: {
          firstName: '',
          lastName: '',
          email: '',
          phone: '',
        },
        deliveryMethod: 'mail',
        deliveryAddress: {
          company: '',
          chamberOfCommerce: '',
          street: '',
          number: '',
          city: '',
          postalCode: '',
          country: 'N',
        },
        billingSameAsDelivery: true,
        billingAddress: null,
      } satisfies FormikValues,
      initialErrors: {},
    },
    msw: {
      handlers: [
        http.get(`${API_ROOT}api/v1/shop/shipping-costs/`, () => {
          return HttpResponse.json({
            price: '11.9',
            weight: '320 g',
          });
        }),
      ],
    },
  },
} satisfies Meta<Args>;

type Story = StoryObj<Args>;

export const Default: Story = {name: 'ShippingCosts'};

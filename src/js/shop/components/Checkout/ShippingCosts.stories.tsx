import type {Meta, StoryObj} from '@storybook/react';
import {useFormikContext} from 'formik';
import {HttpResponse, http} from 'msw';
import {useEffect} from 'react';

import {API_ROOT} from '@/constants.js';
import {withFormik} from '@/storybook/decorators';

import type {FormikValues} from './Delivery';
import ShippingCosts from './ShippingCosts';
import {withCheckout} from './storybook';

interface Args {
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
  decorators: [withFormik, withCheckout],
  args: {
    country: 'N',
  },
  argTypes: {
    country: {
      control: 'inline-radio',
      options: ['N', 'B', 'D'],
    },
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

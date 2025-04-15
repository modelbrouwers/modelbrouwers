import {withFormik} from '@/storybook/decorators';
import type {Meta, StoryObj} from '@storybook/react';

import CountryField from './CountryField';

export default {
  title: 'Components / Forms / CountryField',
  component: CountryField,
  decorators: [withFormik],
  args: {
    name: 'country',
    label: 'Select a country',
    required: true,
  },
  parameters: {
    formik: {
      initialValues: {
        country: 'N',
      },
    },
  },
} satisfies Meta<typeof CountryField>;

type Story = StoryObj<typeof CountryField>;

export const Default: Story = {
  name: 'CountryField',
};

export const Empty: Story = {
  parameters: {
    formik: {
      initialValues: {
        country: '',
      },
    },
  },
};

export const WithError: Story = {
  parameters: {
    formik: {
      initialTouched: {
        country: true,
      },
      initialErrors: {
        country: 'Some error',
      },
    },
  },
};

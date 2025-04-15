import type {Meta, StoryObj} from '@storybook/react';

import {withFormik} from '@/storybook/decorators';

import Radio from './Radio';

export default {
  title: 'Components / Forms / Radio',
  component: Radio,
  decorators: [withFormik],
  args: {
    name: 'example',
    label: 'Example Radio',
    options: [
      {
        value: 'one',
        label: 'One',
        graphic: <i className="fa fa-fw fa-2x fa-bath" />,
      },
      {
        value: 'two',
        label: 'Two',
        graphic: <i className="fa fa-fw fa-2x fa-shower" />,
      },
      {
        value: 'three',
        label: 'Three',
      },
    ],
  },
  parameters: {
    formik: {
      initialValues: {
        example: 'two',
      },
    },
  },
} satisfies Meta<typeof Radio>;

type Story = StoryObj<typeof Radio>;

export const Default: Story = {};

export const WithError: Story = {
  parameters: {
    formik: {
      initialTouched: {
        example: true,
      },
      initialErrors: {
        example: 'Some error',
      },
    },
  },
};

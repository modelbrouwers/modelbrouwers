import type {Meta, StoryObj} from '@storybook/react-webpack5';

import {fn} from 'storybook/test';

import FormField from './FormField';

export default {
  title: 'Components/ Forms / FormField',
  component: FormField,
  args: {
    children: (
      <input
        type="text"
        name="some-field"
        className="form-control"
        value=""
        placeholder="kit number"
        onChange={fn()}
        id="someFieldId"
      />
    ),
    htmlId: 'someFieldId',
    label: 'Some form field',
    required: false,
    labelGrid: 'col-sm-4',
    fieldGrid: 'col-sm-8',
  },
} satisfies Meta<typeof FormField>;

type Story = StoryObj<typeof FormField>;

export const Default: Story = {};

import type {Meta, StoryObj} from '@storybook/react-webpack5';

import Label from './Label';

export default {
  title: 'Components/ Forms / Label',
  component: Label,
  args: {
    label: 'A field label',
    htmlId: 'someFieldId',
    labelGrid: 'col-sm-4',
    required: false,
  },
} satisfies Meta<typeof Label>;

type Story = StoryObj<typeof Label>;

export const Default: Story = {};

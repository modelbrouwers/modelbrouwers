import type {Meta, StoryObj} from '@storybook/react-webpack5';

import {fn} from 'storybook/test';

import {mockGetKitBrands, mockGetKitScales} from '@/kits/mocks';

import {AddKitForm} from './ModelKitAdd';

export default {
  title: 'Kits / AddKitForm',
  component: AddKitForm,
  args: {
    brand: null,
    scale: null,
    name: '',
    kitNumber: '',
    difficulty: '',
    onChange: fn(),
    onSubmit: fn(),
    formId: '',
  },
  parameters: {
    msw: {
      handlers: {
        kitBrands: [mockGetKitBrands()],
        kitScales: [mockGetKitScales()],
      },
    },
  },
} satisfies Meta<typeof AddKitForm>;

type Story = StoryObj<typeof AddKitForm>;

export const Default: Story = {};

export const WithPrepopulatedData: Story = {
  args: {
    brand: {
      id: 1,
      name: 'Revell',
      is_active: true,
    },
    scale: {
      id: 1,
      scale: 48,
      __str__: '1/48',
    },
    name: 'F-4F Phantom II',
    kitNumber: '123456',
    difficulty: '30',
  },
};

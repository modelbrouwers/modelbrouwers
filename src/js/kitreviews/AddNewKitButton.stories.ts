import type {Meta, StoryObj} from '@storybook/react-webpack5';

import {expect, fn, userEvent, within} from 'storybook/test';

import {mockGetKitBrands, mockGetKitScales} from '@/kits/mocks';

import AddNewKitButton from './AddNewKitButton';

export default {
  title: 'Kitreviews / AddNewKitButton',
  component: AddNewKitButton,
  args: {
    onKitAdded: fn(),
  },
  parameters: {
    msw: {
      handlers: {
        kitBrands: [mockGetKitBrands()],
        kitScales: [mockGetKitScales()],
      },
    },
  },
} satisfies Meta<typeof AddNewKitButton>;

type Story = StoryObj<typeof AddNewKitButton>;

export const Initial: Story = {};

export const Clicked: Story = {
  play: async ({canvasElement}) => {
    const canvas = within(canvasElement);
    await userEvent.click(canvas.getByRole('button', {name: 'Add new kit'}));

    const modal = await canvas.findByRole('dialog');
    expect(modal).toBeVisible();

    const nameField = within(modal).getByLabelText('name');
    expect(nameField).toBeVisible();
  },
};

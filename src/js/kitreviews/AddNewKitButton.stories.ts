import type {Meta, StoryObj} from '@storybook/react';
import {expect, fn, userEvent, within} from '@storybook/test';
import {HttpResponse, http} from 'msw';

import {API_ROOT} from '@/constants.js';

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
        kitBrands: [
          http.get(`${API_ROOT}api/v1/kits/brand/`, () =>
            HttpResponse.json([
              {
                id: 1,
                name: 'Revell',
                is_active: true,
              },
            ]),
          ),
        ],
        kitScales: [
          http.get(`${API_ROOT}api/v1/kits/scale/`, () =>
            HttpResponse.json([
              {
                id: 1,
                scale: 48,
                __str__: '1/48',
              },
            ]),
          ),
        ],
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

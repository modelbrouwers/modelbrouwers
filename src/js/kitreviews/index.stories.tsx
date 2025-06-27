import type {Meta, StoryObj} from '@storybook/react';
import {expect, userEvent, within} from '@storybook/test';
import {HttpResponse, http} from 'msw';
import {useEffect} from 'react';

import {API_ROOT} from '@/constants.js';
import type {ListBrandData} from '@/data/kits/brand';
import type {ScaleData} from '@/data/kits/scale';

import Page from './index.js';

interface Args {}

const RenderPage: React.FC = () => {
  useEffect(() => {
    Page.initKitCreate();
  }, []);
  return null;
};

export default {
  title: 'Kitreviews / Index',
  render: () => <RenderPage />,
  decorators: [
    Story => (
      <>
        <div id="find-kit-form__button-add-kit" />
        <div id="add-kit-modal" />
        <Story />
      </>
    ),
  ],
  parameters: {
    msw: {
      handlers: {
        kitBrands: [
          http.get(`${API_ROOT}api/v1/kits/brand/`, () =>
            HttpResponse.json<ListBrandData[]>([
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
            HttpResponse.json<ScaleData[]>([
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
} satisfies Meta<Args>;

type Story = StoryObj<Args>;

export const OpenAddKitModal: Story = {
  play: async ({canvasElement}) => {
    const canvas = within(canvasElement);
    const button = await canvas.findByRole('button', {name: 'Add new kit'});
    expect(button).toBeVisible();

    await userEvent.click(button);
  },
};

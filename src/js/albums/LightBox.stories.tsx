import type {Meta, StoryObj} from '@storybook/react';
import {HttpResponse, http} from 'msw';

import {API_ROOT} from '@/constants.js';

import LightBox from './LightBox';

export default {
  title: 'Albums / LightBox',
  component: LightBox,
  args: {
    albumId: 99,
    page: 1,
    selectedPhotoId: 33,
  },
  parameters: {
    msw: {
      handlers: [
        http.get(`${API_ROOT}api/v1/albums/photo/`, ({request}) =>
          HttpResponse.json({
            count: 20,
            paginate_by: 2,
            previous: null,
            next: `${request.url}&page=2`,
            results: [
              {
                id: 33,
                user: {username: 'BBT'},
                description: 'Image description',
                image: {
                  large: './static/images/thumb.png',
                  thumb: './static/images/thumb.png',
                },
                width: 400,
                height: 320,
                uploaded: '2025-01-01T12:00:00+00:00',
                order: 1,
              },
              {
                id: 34,
                user: {username: 'BBT'},
                description: 'Image 2 description',
                image: {
                  large: './static/images/thumb.png',
                  thumb: './static/images/thumb.png',
                },
                width: 400,
                height: 320,
                uploaded: '2025-01-01T12:00:04+00:00',
                order: 2,
              },
            ],
          }),
        ),
      ],
    },
  },
} satisfies Meta<typeof LightBox>;

type Story = StoryObj<typeof LightBox>;

export const Default: Story = {name: 'LightBox'};

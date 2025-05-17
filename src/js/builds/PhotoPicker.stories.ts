import type {Meta, StoryObj} from '@storybook/react';
import {fn} from '@storybook/test';
import {HttpResponse, http} from 'msw';

import {API_ROOT} from '@/constants.js';

import PhotoPicker from './PhotoPicker';

export default {
  title: 'Builds / PhotoPicker',
  component: PhotoPicker,
  args: {
    albumId: 99,
    selectedPhotoIds: [33],
    onToggle: fn(),
  },
  parameters: {
    msw: {
      handlers: [
        http.get(`${API_ROOT}api/v1/albums/photo/`, ({request}) => {
          const page = parseInt(new URL(request.url).searchParams.get('page') || '1');
          return HttpResponse.json({
            count: 4,
            paginate_by: 2,
            previous: null,
            next: `${request.url}&page=2`,
            results: [
              {
                id: 10 * page + 1,
                user: {username: 'BBT'},
                description: `Page ${page}, photo 1`,
                image: {
                  large: './static/images/thumb.png',
                  thumb: './static/images/thumb.png',
                },
                width: 400,
                height: 320,
                uploaded: '2025-01-01T12:00:00+00:00',
                order: 10 * page + 1,
              },
              {
                id: 10 * page + 2,
                user: {username: 'BBT'},
                description: `Page ${page}, photo 2`,
                image: {
                  large: './static/images/thumb.png',
                  thumb: './static/images/thumb.png',
                },
                width: 400,
                height: 320,
                uploaded: '2025-01-01T12:00:04+00:00',
                order: 10 * page + 2,
              },
            ],
          });
        }),
      ],
    },
  },
} satisfies Meta<typeof PhotoPicker>;

type Story = StoryObj<typeof PhotoPicker>;

export const Default: Story = {
  name: 'PhotoPicker',
};

import type {Meta, StoryObj} from '@storybook/react';
import {expect, fn, userEvent, within} from '@storybook/test';
import {HttpResponse, http} from 'msw';

import {API_ROOT} from '@/constants.js';

import SideBar from './SideBar';

export default {
  title: 'Forum / Albums / Sidebar',
  component: SideBar,
  args: {
    onInsertPhoto: fn(),
  },
} satisfies Meta<typeof SideBar>;

type Story = StoryObj<typeof SideBar>;

export const Opened: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get(`${API_ROOT}api/v1/my/albums/`, () =>
          HttpResponse.json([
            {
              id: 1,
              user: {username: 'BBT'},
              title: 'F-4 Phantom II',
              description: 'Build report pictures',
              public: true,
              topic: {
                topic_id: 2,
                is_dead: false,
                age: '8 years, 6 months',
                text_dead: '',
                topic_title: 'F-4 Phantom II',
                last_post_time: 1478634552,
                create_time: 1455565677,
                forum: 23,
                author: 862,
              },
            },
            {
              id: 11613,
              user: {username: 'BBT'},
              title: 'Handleiding albums',
              description: '',
              public: true,
              topic: null,
            },
          ]),
        ),
        http.get(`${API_ROOT}api/v1/my/photos/`, () =>
          HttpResponse.json({
            count: 2,
            previous: null,
            next: null,
            results: [
              {
                id: 100,
                user: 1,
                description: 'one',
                image: {
                  large: './static/images/thumb.png',
                  thumb: './static/images/thumb.png',
                },
              },
              {
                id: 103,
                user: 1,
                description: 'two',
                image: {
                  large: './static/images/thumb.png',
                  thumb: './static/images/thumb.png',
                },
              },
            ],
          }),
        ),
        http.get(`${API_ROOT}api/v1/my/photos/:id/`, ({params}) =>
          HttpResponse.json({
            id: params.id,
            user: 1,
            description: 'one',
            image: {
              large: './static/images/thumb.png',
              thumb: './static/images/thumb.png',
            },
          }),
        ),
      ],
    },
  },

  play: async ({canvasElement}) => {
    const canvas = within(canvasElement);

    const button = canvas.getByRole('button', {name: "Toon albums en foto's"});
    await userEvent.click(button);

    expect(await canvas.findByRole('heading', {name: 'Photos'})).toBeVisible();
    expect(await canvas.findAllByRole('img')).toHaveLength(2);

    const photoPreviews = canvas.getAllByRole('link', {name: 'Insert photo'});
    await userEvent.click(photoPreviews[0]);
  },
};

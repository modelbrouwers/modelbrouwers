import type {Meta, StoryObj} from '@storybook/react';
import {HttpResponse, http} from 'msw';
import {useEffect} from 'react';

import {API_ROOT} from '@/constants.js';

import {fetchAndDisplayAnnouncements} from './announcement';

interface Args {}

const Render: React.FC = () => {
  useEffect(() => {
    fetchAndDisplayAnnouncements();
  }, []);
  return null;
};

export default {
  title: 'Forum / Announcement',
  render: () => <Render />,
  decorators: Story => (
    <>
      <div id="announcement" />
      <Story />
    </>
  ),
} satisfies Meta<Args>;

type Story = StoryObj<Args>;

export const HasAnnouncement: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get(`${API_ROOT}api/v1/forum_tools/announcement/`, () =>
          HttpResponse.json({
            html: '<p>An announcement from the backend</p>',
          }),
        ),
      ],
    },
  },
};

export const NoAnnouncement: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get(`${API_ROOT}api/v1/forum_tools/announcement/`, () =>
          HttpResponse.json({html: null}),
        ),
      ],
    },
  },
};

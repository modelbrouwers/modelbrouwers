import type {Meta, StoryObj} from '@storybook/react';
import {HttpResponse, http} from 'msw';

import {API_ROOT} from '@/constants.js';

import GroupBuildInset from './GroupBuildInset';

export default {
  title: 'Group builds / Inset',
  component: GroupBuildInset,
  args: {
    id: 99,
  },
  parameters: {
    msw: {
      handlers: [
        http.get(`${API_ROOT}api/v1/groupbuilds/groupbuild/:id/`, ({params}) =>
          HttpResponse.json({
            id: params.id,
            theme: 'Example groupbuild',
            url: '#some-url',
            description: 'A description\n\nwith newlines',
            start: '2025-01-01',
            end: '2025-07-01',
            status: 'Proposal',
            rules: '',
            rules_topic: {
              title: 'The topic',
              url: '#topic',
            },
            participants: [
              {
                id: 999,
                model_name: 'YF-4E Phantom II',
                username: 'BBT',
                topic: {title: 'Rhino', url: '#topic'},
                finished: false,
              },
            ],
          }),
        ),
      ],
    },
  },
} satisfies Meta<typeof GroupBuildInset>;

type Story = StoryObj<typeof GroupBuildInset>;

export const Default: Story = {
  name: 'Inset',
};

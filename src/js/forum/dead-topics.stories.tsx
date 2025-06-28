import type {Meta, StoryObj} from '@storybook/react';
import {expect, userEvent, within} from '@storybook/test';
import {HttpResponse, http} from 'msw';
import {useEffect} from 'react';

import {API_ROOT} from '@/constants.js';

import ForumTools from './forum-tools.js';

interface Args {}

const Render: React.FC = () => {
  useEffect(() => {
    ForumTools.initDeadTopics();
  }, []);
  return null;
};

export default {
  title: 'Forum / Dead topics',
  render: () => <Render />,
  decorators: [
    Story => (
      <div>
        <a href="#newpost" className="new-post" data-topic-id="123">
          Add post
        </a>
        <div id="dead_topic" data-post-reply-url="#" />
        <Story />
      </div>
    ),
  ],
} satisfies Meta<Args>;

type Story = StoryObj<Args>;

export const Trigger: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get(`${API_ROOT}api/v1/forum_tools/topic/:id/`, ({params}) =>
          HttpResponse.json({
            topic_id: params.id,
            forum: 123,
            topic_title: 'Some topic',
            last_post_time: Number(new Date()),
            create_time: Number(new Date()),
            author: 99,
            is_dead: true,
            age: '6 months',
            text_dead: 'This topic is no longer active',
          }),
        ),
      ],
    },
  },
  play: async ({canvasElement}) => {
    const canvas = within(canvasElement);

    const addPost = canvas.getByRole('link', {name: 'Add post'});
    await userEvent.click(addPost);

    const dialogElement = await canvas.findByRole('dialog');
    const dialog = within(dialogElement);

    expect(await dialog.findByText('This topic is no longer active')).toBeVisible();
  },
};

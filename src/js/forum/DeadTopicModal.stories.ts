import type {Meta, StoryObj} from '@storybook/react';
import {fn} from '@storybook/test';

import DeadTopicModal from './DeadTopicModal';

export default {
  title: 'Forum / Dead topics / Modal',
  component: DeadTopicModal,
  args: {
    message: `
      This topic has been inactive since 6 months. It may be better to send the
      author a private message instead of bumping it.
    `,
    onRequestClose: fn(),
    replyTopicUrl: '#',
  },
} satisfies Meta<typeof DeadTopicModal>;

type Story = StoryObj<typeof DeadTopicModal>;

export const Modal: Story = {};

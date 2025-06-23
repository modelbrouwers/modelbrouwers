import type {Meta, StoryObj} from '@storybook/react';
import {expect, fn, userEvent, within} from '@storybook/test';
import {useState} from 'react';

import Modal from './Modal';

export default {
  title: 'General purpose / Modal',
  component: Modal,
  args: {
    isOpen: true,
    onRequestClose: fn(),
    children: 'Modal body',
  },
} satisfies Meta<typeof Modal>;

type Story = StoryObj<typeof Modal>;

export const Default: Story = {};

export const Title: Story = {
  args: {
    title: 'A modal title',
  },
};

export const Interaction: Story = {
  render: () => {
    const [isOpen, setIsOpen] = useState<boolean>(false);

    return (
      <>
        <button type="button" onClick={() => setIsOpen(true)}>
          Open
        </button>
        <Modal isOpen={isOpen} onRequestClose={() => setIsOpen(false)} title="Interaction">
          <p>Modal content</p>
        </Modal>
      </>
    );
  },
  play: async ({canvasElement}) => {
    const canvas = within(canvasElement);

    const button = canvas.getByRole('button', {name: 'Open'});
    await userEvent.click(button);

    expect(canvas.getByRole('dialog')).toBeVisible();

    await userEvent.keyboard('Tab');
    const closeButton = canvas.getByRole('button', {name: 'Close'});
    expect(closeButton).toHaveFocus();

    await userEvent.click(closeButton);
    expect(canvas.queryByRole('dialog')).not.toBeInTheDocument();
  },
};

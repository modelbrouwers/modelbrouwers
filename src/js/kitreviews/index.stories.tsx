import type {Meta, StoryObj} from '@storybook/react';
import {expect, userEvent, within} from '@storybook/test';
import {useEffect} from 'react';

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
        <button className="button button--icon button--orange find-kit-form__button-add-kit">
          <i className="fa fa-plus"></i> Add new kit
        </button>
        <Story />
      </>
    ),
  ],
} satisfies Meta<Args>;

type Story = StoryObj<Args>;

export const OpenAddKitModal: Story = {
  play: async ({canvasElement}) => {
    const canvas = within(canvasElement);
    await userEvent.click(canvas.getByRole('button', {name: 'Add new kit'}));

    const modal = await canvas.findByRole('dialog');
    expect(modal).toBeVisible();

    const nameField = within(modal).getByLabelText('name');
    expect(nameField).toBeVisible();
  },
};

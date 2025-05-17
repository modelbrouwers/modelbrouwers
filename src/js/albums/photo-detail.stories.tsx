import type {Meta, StoryObj} from '@storybook/react';
import {userEvent, within} from '@storybook/test';
// @ts-expect-error
import $ from 'jquery';
import {HttpResponse, http} from 'msw';
import {useEffect} from 'react';

import {API_ROOT} from '@/constants.js';

import Page from './index.js';

interface Args {}

const Render: React.FC = () => {
  useEffect(() => {
    Page.initControls();
    $('.controls [data-toggle="popover"]').popover();
  }, []);
  return null;
};

export default {
  title: 'Albums / Photo detail',
  render: () => <Render />,
  decorators: [
    Story => (
      <article className="photo">
        <figure data-id="123">
          <img src="./static/images/thumb.png" className="img-responsive" />
          <figcaption>
            <p>Optional photo description</p>
          </figcaption>

          <div className="controls-group top right">
            <div className="controls">
              <i
                className="fa fa-fw fa-compress fa-2x"
                data-action="compress"
                data-trigger="hover focus"
                data-toggle="popover"
                data-placement="auto top"
                data-content="Collapses the image if it is higher than the browser window"
              />
            </div>
            <div className="controls">
              <i
                className="fa fa-fw fa-rotate-left fa-2x"
                data-action="rotate-left"
                data-testid="rotate-left"
                data-trigger="hover focus"
                data-toggle="popover"
                data-placement="auto top"
                data-content="Rotate the image to the left"
              />
              <i
                className="fa fa-fw fa-rotate-right fa-2x"
                data-action="rotate-right"
                data-testid="rotate-right"
                data-trigger="hover focus"
                data-toggle="popover"
                data-placement="auto top"
                data-content="Rotate the image to the right"
              />
            </div>
          </div>
        </figure>
        <Story />
      </article>
    ),
  ],
  parameters: {
    msw: {
      handlers: [
        http.patch(`${API_ROOT}api/v1/albums/photo/:id/rotate/`, ({params}) =>
          HttpResponse.json({
            id: params.id,
            user: {username: 'BBT'},
            description: '',
            image: {
              thumb: './static/images/thumb.png',
              large: './static/images/thumb.png',
            },
            width: 400,
            height: 320,
            uploaded: '2025-01-01T12:00:00+00:00',
            order: 1,
          }),
        ),
      ],
    },
  },
} satisfies Meta<Args>;

type Story = StoryObj<Args>;

export const RotateLeft: Story = {
  play: async ({canvasElement}) => {
    const canvas = within(canvasElement);

    await userEvent.click(canvas.getByTestId('rotate-left'));
  },
};

export const RotateRight: Story = {
  play: async ({canvasElement}) => {
    const canvas = within(canvasElement);

    await userEvent.click(canvas.getByTestId('rotate-right'));
  },
};

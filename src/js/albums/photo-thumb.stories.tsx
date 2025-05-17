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
  title: 'Albums / Photo thumb',
  render: () => <Render />,
  decorators: [
    Story => (
      <article className="col-sm-6 col-md-3" data-id="123" style={{marginTop: '60px'}}>
        <a href="#" className="thumbnail album-photo" data-id="123">
          <img src="./static/images/thumb.png" className="img-responsive" />
        </a>
        <ul className="list-inline controls text-right">
          <li
            data-toggle="popover"
            data-content="Set as cover"
            data-trigger="hover"
            data-placement="top"
            className="set-cover"
          >
            <a href="#" data-action="set-cover" data-testid="set-cover">
              <i className="fa fa-fw fa-picture-o" />
            </a>
          </li>
          <li
            data-toggle="popover"
            data-content="Edit photo"
            data-trigger="hover"
            data-placement="top"
            data-container="body"
          >
            <a href="#">
              <i className="fa fa-fw fa-pencil-square-o" />
            </a>
          </li>
          <li
            data-toggle="popover"
            data-content="Delete photo"
            data-trigger="hover"
            data-placement="top"
            data-container="body"
          >
            <a href="#">
              <i className="fa fa-fw fa-trash" />
            </a>
          </li>
        </ul>
        <Story />
      </article>
    ),
  ],
  parameters: {
    msw: {
      handlers: [
        http.post(`${API_ROOT}api/v1/my/photos/:id/set_cover/`, ({params}) =>
          HttpResponse.json({
            id: params.id,
            user: 1,
            description: '',
            image: {
              thumb: './static/images/thumb.png',
              large: './static/images/thumb.png',
            },
          }),
        ),
      ],
    },
  },
} satisfies Meta<Args>;

type Story = StoryObj<Args>;

export const SetAsCover: Story = {
  play: async ({canvasElement}) => {
    const canvas = within(canvasElement);

    const setAsCoverLink = canvas.getByTestId('set-cover');
    await userEvent.click(setAsCoverLink);
  },
};

import type {Preview} from '@storybook/react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'font-awesome/css/font-awesome.min.css';
import {initialize, mswLoader} from 'msw-storybook-addon';

import '../src/sass/screen.scss';
import {reactIntl} from './reactIntl.ts';

initialize({onUnhandledRequest: 'bypass'});

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    reactIntl,
  },

  loaders: [mswLoader],

  initialGlobals: {
    locale: reactIntl.defaultLocale,
    locales: {
      en: 'English',
      nl: 'Nederlands',
      de: 'Deutsch',
    },
  },
};

export default preview;

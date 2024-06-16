import type { Preview } from "@storybook/react";
import { initialize, mswLoader } from "msw-storybook-addon";

import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "../src/sass/screen.scss";

import { reactIntl } from "./reactIntl.ts";

initialize();

const preview: Preview = {
  globals: {
    locale: reactIntl.defaultLocale,
    locales: {
      en: "English",
      nl: "Nederlands",
      de: "Deutsch",
    },
  },
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
};

export default preview;

import type { StorybookConfig } from "@storybook/react-webpack5";
import { EnvironmentPlugin } from "webpack";

const config: StorybookConfig = {
  core: {
    disableTelemetry: true,
    disableWhatsNewNotifications: true,
  },
  stories: ["../src/**/*.mdx", "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
  addons: [
    "@storybook/addon-webpack5-compiler-babel",
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@chromatic-com/storybook",
    "@storybook/addon-interactions",
    {
      name: "@storybook/addon-styling-webpack",
      options: {
        rules: [
          // Replaces existing CSS rules with given rule
          {
            test: /\.css$/,
            use: [
              "style-loader",
              { loader: "css-loader", options: { url: false } },
            ],
          },
          // Replaces any existing Sass rules with given rules
          {
            test: /\.s[ac]ss$/i,
            use: [
              "style-loader",
              { loader: "css-loader", options: { url: false } },
              {
                loader: "sass-loader",
                options: {
                  implementation: require.resolve("sass"),
                },
              },
            ],
          },
        ],
      },
    },
    "storybook-react-intl",
  ],
  framework: {
    name: "@storybook/react-webpack5",
    options: {},
  },
  staticDirs: [
    { from: "../static/fonts", to: "fonts" },
    { from: "../static/font-awesome/fonts", to: "fonts" },
    { from: "../static/images", to: "static/images" },
  ],

  webpackFinal: (config, options) => {
    if (!config.plugins) config.plugins = [];
    config.plugins.push(
      new EnvironmentPlugin({
        BACKEND_SERVER: "http://localhost:8000/",
        STATIC_ROOT: "/static",
      }),
    );
    return config;
  },
};
export default config;

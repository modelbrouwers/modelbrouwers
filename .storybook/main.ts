import type { StorybookConfig } from "@storybook/react-webpack5";
import { EnvironmentPlugin } from "webpack";
import path from "path";

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
    "storybook-addon-remix-react-router",
  ],
  framework: {
    name: "@storybook/react-webpack5",
    options: {},
  },
  staticDirs: [
    { from: "../static/fonts", to: "fonts" },
    { from: "../static/font-awesome/fonts", to: "fonts" },
    { from: "../static/images", to: "static/images" },
    { from: "../public", to: "" },
  ],

  webpackFinal: (config, options) => {
    if (!config.plugins) config.plugins = [];
    config.plugins.push(
      new EnvironmentPlugin({
        BACKEND_SERVER: "http://localhost:8000/",
        STATIC_ROOT: "/static",
      }),
    );

    if (!config.resolve) config.resolve = {};
    if (!config.resolve.modules) config.resolve.modules = [];
    config.resolve.modules.push(path.resolve(__dirname, "..", "src/js/"));

    return config;
  },
};
export default config;

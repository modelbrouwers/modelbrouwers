// This file has been automatically migrated to valid ESM format by Storybook.
import type {StorybookConfig} from '@storybook/react-webpack5';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
import path, {dirname} from 'path';
import TsconfigPathsPlugin from 'tsconfig-paths-webpack-plugin';
import webpack from 'webpack';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const require = createRequire(import.meta.url);

const {EnvironmentPlugin, ProvidePlugin} = webpack;

const config: StorybookConfig = {
  core: {
    disableTelemetry: true,
    disableWhatsNewNotifications: true,
  },

  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],

  addons: [
    '@storybook/addon-webpack5-compiler-babel',
    '@storybook/addon-links',
    {
      name: '@storybook/addon-styling-webpack',
      options: {
        rules: [
          // Replaces existing CSS rules with given rule
          {
            test: /\.css$/,
            use: ['style-loader', {loader: 'css-loader', options: {url: false}}],
          },
          // Replaces any existing Sass rules with given rules
          {
            test: /\.s[ac]ss$/i,
            use: [
              'style-loader',
              {loader: 'css-loader', options: {url: false}},
              {
                loader: 'sass-loader',
                options: {
                  implementation: require.resolve('sass'),
                },
              },
            ],
          },
        ],
      },
    },
    'storybook-react-intl',
    'storybook-addon-remix-react-router',
    '@storybook/addon-docs',
  ],

  framework: {
    name: '@storybook/react-webpack5',
    options: {},
  },

  staticDirs: [
    {from: '../static/fonts', to: 'fonts'},
    {from: '../static/font-awesome/fonts', to: 'fonts'},
    {from: '../static/images', to: 'static/images'},
    {from: '../public', to: ''},
  ],

  webpackFinal: (config, options) => {
    if (!config.plugins) config.plugins = [];
    config.plugins.push(
      new EnvironmentPlugin({
        BACKEND_SERVER: 'http://localhost:8000/',
        STATIC_ROOT: '/static',
      }),
    );
    config.plugins.push(
      new ProvidePlugin({
        jQuery: 'jquery',
        $: 'jquery',
        'window.jQuery': 'jquery',
      }),
    );

    if (!config.resolve) config.resolve = {};
    if (!config.resolve.modules) config.resolve.modules = [];
    config.resolve.modules.push(path.resolve(__dirname, '..', 'src/js/'));
    if (!config.resolve.plugins) config.resolve.plugins = [];
    config.resolve.plugins.push(new TsconfigPathsPlugin());

    return config;
  },

  docs: {},

  typescript: {
    reactDocgen: 'react-docgen-typescript',
  },
};
export default config;

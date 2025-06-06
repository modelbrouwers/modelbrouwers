const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const argv = require('yargs').argv;
const webpack = require('webpack');
const path = require('path');
const transform = require('@formatjs/ts-transformer').transform;
const TsconfigPathsPlugin = require('tsconfig-paths-webpack-plugin');

// Set isProduction based on environment or argv.

let isProduction = process.env.NODE_ENV === 'production';
if (argv.production) {
  isProduction = true;
}

/**
 * Webpack configuration
 * Run using "webpack"
 */
module.exports = {
  // Path to the js entry point (source)
  entry: {
    // Javascript
    main: `${__dirname}/src/js/index.js`,
    forum: `${__dirname}/src/js/forum.js`,
    // CSS
    'screen-css': `${__dirname}/src/sass/screen.scss`,
    'forum-css': `${__dirname}/src/sass/forum.scss`,
    'print-brouwersdag-css': `${__dirname}/src/sass/print_brouwersdag.scss`,
  },

  // Path to the (transpiled) js & CSS
  output: {
    path: `${__dirname}/src/static/bundles/`,
    filename: '[name].js', // file
    chunkFilename: '[name].bundle.js',
    publicPath: '/static/bundles/',
  },

  plugins: [
    new MiniCssExtractPlugin(),
    new webpack.EnvironmentPlugin({
      BACKEND_SERVER: '/',
      STATIC_ROOT: '/static',
    }),
    // Necessary for some libs that rely on global jQuery to work (e.g. bootstrap)
    new webpack.ProvidePlugin({
      jQuery: 'jquery',
      $: 'jquery',
      'window.jQuery': 'jquery',
    }),
  ],

  module: {
    rules: [
      {
        test: /\.(png|svg|jpg|gif)$/,
        use: ['file-loader'],
      },
      {
        test: /\.tsx?$/,
        // exclude: /node_modules/,
        use: {
          loader: 'ts-loader',
          options: {
            getCustomTransformers() {
              return {
                before: [
                  transform({
                    overrideIdFn: '[sha512:contenthash:base64:6]',
                  }),
                ],
              };
            },
          },
        },
      },
      {
        test: /\.js$/,
        exclude: /(node_modules)/,
        use: {
          loader: 'babel-loader',
          options: {
            cacheDirectory: true,
          },
        },
      },
      {
        test: /\.(woff|woff2|eot|ttf)$/,
        loader: 'url-loader',
      },
      // scss
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          // Writes css files.
          MiniCssExtractPlugin.loader,

          // Loads CSS files.
          {
            loader: 'css-loader',
            options: {
              url: false,
            },
          },

          // Runs postcss configuration (postcss.config.js).
          {
            loader: 'postcss-loader',
          },

          // Compiles .scss to .css.
          {
            loader: 'sass-loader',
            options: {
              sassOptions: {
                comments: false,
                style: 'compressed',
              },
              sourceMap: argv.sourcemap,
            },
          },
        ],
      },
    ],
  },

  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
    modules: [path.resolve(__dirname, 'src/js/'), 'node_modules'],
    plugins: [new TsconfigPathsPlugin()],
  },

  mode: isProduction ? 'production' : 'development',

  // Use --sourcemap to generate sourcemap.
  devtool: argv.sourcemap ? 'source-map' : false,
};

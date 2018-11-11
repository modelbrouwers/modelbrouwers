var paths = require('./build/paths');
var webpack = require('webpack');
/**
 * Webpack configuration
 * Run using "webpack"
 */
console.log('ENTRY', __dirname + '/' + paths.jsEntry)
module.exports = {
    // Path to the js entry point (source)
    entry: __dirname + '/' + paths.jsEntry,

    // Path to the (transpiled) js
    output: {
        publicPath: __dirname + '/' + paths.jsDir,
        path: __dirname + '/' + paths.jsDir, // directory
        // filename: '[name].bundle.js', // file
        //  chunkFilename: '[name].bundle.js'
    },

    module: {
        rules: [
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: [
                    'file-loader'
                ]
            },
            {
                test: /\.js$/,
                exclude: /(node_modules)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
                        plugins: ["@babel/plugin-syntax-dynamic-import"],
                        cacheDirectory: true,
                    }
                }
            },
            {
                test: /\.(woff|woff2|eot|ttf)$/,
                loader: 'url-loader'
            }
        ],
    },

    devtool: 'inline-source-map',


    optimization: {
        minimize: false
    },

    watch: true
};

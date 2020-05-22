const paths = require("./build/paths");
const webpack = require("webpack");
const exec = require("child_process").exec;
/**
 * Webpack configuration
 * Run using "webpack"
 */

let entry = {};
for (let key in paths.jsEntry) {
    entry[key] = __dirname + "/" + paths.jsEntry[key];
}
// console.log(entry);

var config = {
    // Path to the js entry point (source)
    entry: entry,

    // Path to the (transpiled) js
    output: {
        publicPath: __dirname + "/" + paths.jsDir,
        path: __dirname + "/" + paths.jsDir, // directory
        filename: "[name].js" // file
        //  chunkFilename: '[name].bundle.js'
    },

    module: {
        rules: [
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: ["file-loader"]
            },
            {
                test: /\.js$/,
                exclude: /(node_modules)/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env"],
                        plugins: [
                            [
                                "@babel/plugin-proposal-decorators",
                                { legacy: true }
                            ],
                            [
                                "@babel/plugin-proposal-class-properties",
                                { loose: true }
                            ],
                            "@babel/plugin-syntax-dynamic-import"
                        ],
                        cacheDirectory: true
                    }
                }
            },
            {
                test: /\.(woff|woff2|eot|ttf)$/,
                loader: "url-loader"
            }
        ]
    },

    optimization: {
        minimize: false
    },

    // Necessary for some libs that rely on global jQuery to work (e.g. Typeahead)
    plugins: [
        new webpack.EnvironmentPlugin({
            BACKEND_SERVER: "/",
            STATIC_ROOT: "/static"
        }),
        new webpack.ProvidePlugin({
            jQuery: "jquery",
            $: "jquery",
            "window.jQuery": "jquery"
        })
    ]
};

module.exports = (env, argv) => {

    if ( argv.mode === "development" ) {
        config.devtool = "inline-source-map";
    } else if ( argv.mode === "production" ) {
        // no devtool
    }

    return config;
};

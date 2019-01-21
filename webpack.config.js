var paths = require("./build/paths");
var webpack = require("webpack");
/**
 * Webpack configuration
 * Run using "webpack"
 */

let entry = {};
for (let key in paths.jsEntry) {
    entry[key] = __dirname + "/" + paths.jsEntry[key];
}
console.log(entry);

module.exports = {
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
                            "@babel/plugin-syntax-dynamic-import",
                            "@babel/plugin-proposal-class-properties",
                            [
                                "@babel/plugin-proposal-decorators",
                                {
                                    decoratorsBeforeExport: true
                                }
                            ]
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

    devtool: "inline-source-map",

    optimization: {
        minimize: false
    },

    // Necessary for some libs that rely on global jQuery to work (e.g. Typeahead)
    plugins: [
        new webpack.EnvironmentPlugin({
            BACKEND_SERVER: "/"
        }),
        new webpack.ProvidePlugin({
            jQuery: "jquery",
            $: "jquery",
            "window.jQuery": "jquery"
        })
    ]
};

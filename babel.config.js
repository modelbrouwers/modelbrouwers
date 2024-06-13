module.exports = {
  presets: [
    "@babel/preset-env",
    "@babel/preset-typescript",
    ["@babel/preset-react", { runtime: "automatic" }],
  ],
  plugins: [
    [
      "formatjs",
      {
        idInterpolationPattern: "[sha512:contenthash:base64:6]",
        ast: true,
      },
    ],
    ["@babel/plugin-proposal-decorators", { legacy: true }],
    "@babel/plugin-transform-runtime",
  ],
};

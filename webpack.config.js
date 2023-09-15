const path = require("path");

module.exports = {
  mode: "development",
  entry: "./shiba_inc/js/post_root.jsx",
  output: {
    path: path.join(__dirname, "/shiba_inc/static/js/"),
    filename: "post_bundle.js",
  },
  devtool: "source-map",
  module: {
    rules: [
      {
        // Test for js or jsx files
        test: /\.jsx?$/,
        // Exclude external modules from loader tests
        exclude: /node_modules/,
        loader: "babel-loader",
        options: {
          presets: ["@babel/preset-env", "@babel/preset-react"],
          plugins: ["@babel/transform-runtime"],
        },
      },
    ],
  },
  resolve: {
    extensions: [".js", ".jsx"],
  },
};

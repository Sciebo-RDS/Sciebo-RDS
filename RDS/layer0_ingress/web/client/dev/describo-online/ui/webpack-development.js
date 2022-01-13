const path = require("path");
const { merge } = require("webpack-merge");
const common = require("./webpack-common");
const CopyPlugin = require("copy-webpack-plugin");

const configuration = merge(common, {
    mode: "development",
    devtool: "eval-source-map",
    devServer: {
        contentBase: path.join(__dirname, "dist"),
        compress: true,
        host: "0.0.0.0",
        port: 9000,
        historyApiFallback: true,
        writeToDisk: true,
        hot: true,
    },
});

module.exports = configuration;

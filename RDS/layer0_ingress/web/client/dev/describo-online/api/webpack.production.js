const path = require("path");
const nodeExternals = require("webpack-node-externals");
const CopyPlugin = require("copy-webpack-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

module.exports = {
    target: "node",
    mode: "production",
    entry: "./index.js",
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: "server.bundle.js",
    },
    externals: [nodeExternals()],
    plugins: [
        new CleanWebpackPlugin(),
        new CopyPlugin({
            patterns: [
                { from: "package.json", to: "package.json" },
                { from: "package-lock.json", to: "package-lock.json" },
            ],
        }),
    ],
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: "vue-loader",
            },
            {
                test: /\.js$/,
                loader: "babel-loader",
                exclude: /node_modules/,
            },
        ],
    },
    resolve: {
        alias: {
            src: path.resolve(__dirname, "src"),
        },
    },
};

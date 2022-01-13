const { merge } = require("webpack-merge");
const common = require("./webpack-common");
const TerserPlugin = require("terser-webpack-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

const configuration = merge(common, {
    mode: "production",
    optimization: {
        minimize: true,
        minimizer: [new TerserPlugin(), new CssMinimizerPlugin()],
    },
    output: {
        publicPath: "/",
    },
});

module.exports = configuration;

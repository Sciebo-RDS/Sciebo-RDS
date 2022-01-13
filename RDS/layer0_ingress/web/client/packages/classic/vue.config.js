const Dotenv = require('dotenv-webpack');
const envPath = function () {
  return (!process.env.NODE_ENV || (process.env.NODE_ENV === 'development')) ?
    '../../../.env' :
    `../../../.env.${process.env.NODE_ENV}`;
}

const dotenvArgs = {
  expand: true,
  path: envPath()
};

module.exports = {
  transpileDependencies: [
    'vuetify',
    'vue-oidc-client'
  ],
  filenameHashing: false,
  productionSourceMap: false,
  devServer: {
    proxy: 'http://localhost:8080'
  },
  configureWebpack: {
    plugins: [
      new Dotenv(dotenvArgs)
    ],
  },
  chainWebpack: config => {
    config.optimization.splitChunks(false)
  },
  publicPath: "/apps/rds"
}

const path = require('path')
const { TEST_MODE } = process.env

/*
 * For a detailed explanation regarding each configuration property, visit:
 * https://jestjs.io/docs/en/configuration.html
 */

module.exports = {
  collectCoverageFrom: [
    '<rootDir>/src/**/*.{vue, js}',
    '!<rootDir>/src/main.js',
    '!<rootDir>/src/services/auth.js',
    '!<rootDir>/src/assets/**/*'
  ],
  coverageDirectory: '<rootDir>/coverage',
  moduleFileExtensions: ['js', 'vue'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^.+\\.(css|scss)$': 'babel-jest'
  },
  modulePaths: ['<rootDir>'],
  rootDir: path.resolve(__dirname, './'),
  setupFiles: [`<rootDir>/tests/${TEST_MODE}/config/jest.init.js`],
  snapshotSerializers: ['jest-serializer-vue'],
  testMatch:
    TEST_MODE === 'integration'
      ? ['**/tests/integration/specs/**/*.spec.js']
      : ['**/tests/unit/**/*.spec.js'],
  transform: {
    '^.+\\.js$': 'babel-jest',
    '^.+\\.vue$': 'vue-jest',
    '^.+\\.(jpg|ico|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$':
      '<rootDir>/__mocks__/file.js'
  },
  transformIgnorePatterns: ['node_modules/(?!lodash-es/.*)']
}

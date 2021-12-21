import Vue from 'vue'
import { config } from '@vue/test-utils'
import fetchMock from 'jest-fetch-mock'
fetchMock.enableMocks()

Vue.config.language = 'en'

config.mocks = {
  $gettext: (str) => str,
  $gettextInterpolate: (str) => str
}

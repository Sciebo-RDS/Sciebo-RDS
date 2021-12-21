import Vue from 'vue'
import fetchMock from 'jest-fetch-mock'
import ODS from 'owncloud-design-system'
import { config } from '@vue/test-utils'
import { listResources } from '../../helpers/mocks'
fetchMock.enableMocks()

Vue.use(ODS)
Vue.config.language = 'en'

config.mocks = {
  $client: {
    files: {
      list: listResources
    }
  },
  $gettext: (str) => str,
  $gettextInterpolate: (str) => str,
  $ngettext: (arg) => {
    return arg[2].length > 1 ? arg[1] : arg[0]
  },
  $language: {
    current: 'en_US'
  }
}

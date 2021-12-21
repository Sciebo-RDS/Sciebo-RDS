<template>
  <div id="oc-file-picker" tabindex="-1" @keyup.esc="cancel">
    <div
      v-if="state === 'loading'"
      class="uk-height-1-1 uk-width-1-1 uk-flex uk-flex-middle uk-flex-center oc-border"
    >
      <oc-spinner :aria-label="$gettext('Loading ownCloud File Picker')" />
    </div>
    <login v-if="state === 'unauthorized'" key="login-form" @login="authenticate" />
    <file-picker
      v-if="state === 'authorized'"
      key="file-picker"
      class="uk-height-1-1"
      :variation="variation"
      :select-btn-label="selectBtnLabel"
      :is-select-btn-displayed="isSelectBtnDisplayed"
      :cancel-btn-label="cancelBtnLabel"
      :is-initial-focus-enabled="isInitialFocusEnabled"
      @update="selectResources"
      @select="emitSelectBtnClick"
      @cancel="cancel"
      @folderLoaded="onFolderLoaded"
    />
  </div>
</template>

<script>
import sdk from 'owncloud-sdk'
import DesignSystem from 'owncloud-design-system'
import VueGettext from 'vue-gettext'
import merge from 'lodash-es/merge'

/* global Vue */
if (!Vue.prototype.$client) {
  Vue.prototype.$client = new sdk()
}

import initVueAuthenticate from './services/auth'

import { loadConfig } from './helpers/config'

import filePickerTranslations from '../l10n/translations.json'
import odsTranslations from 'owncloud-design-system/dist/system/translations.json'

import FilePicker from './components/FilePicker.vue'
import Login from './components/Login.vue'

if (!Vue.prototype.$gettext) {
  const supportedLanguages = {
    en: 'English',
    de: 'Deutsch',
    es: 'Español',
    cs: 'Czech',
    fr: 'Français',
    it: 'Italiano',
    gl: 'Galego'
  }
  const translations = merge({}, filePickerTranslations, odsTranslations)

  Vue.use(VueGettext, {
    availableLanguages: supportedLanguages,
    defaultLanguage: navigator.language.substring(0, 2),
    translations,
    silent: true
  })
}

export default {
  name: 'App',

  components: {
    FilePicker,
    Login
  },

  props: {
    variation: {
      type: String,
      required: true,
      validator: (value) => value === 'resource' || value === 'location'
    },
    configLocation: {
      type: String,
      required: false,
      default: () => window.location.origin + '/file-picker-config.json'
    },
    bearerToken: {
      type: String,
      required: false,
      default: null
    },
    configObject: {
      type: [Object, String],
      required: false,
      default: null
    },
    isSdkProvided: {
      type: Boolean,
      required: false,
      default: false
    },
    selectBtnLabel: {
      type: String,
      required: false,
      default: null
    },
    isSelectBtnDisplayed: {
      type: Boolean,
      required: false,
      default: true
    },
    cancelBtnLabel: {
      type: String,
      required: false,
      default: null
    },
    isOdsProvided: {
      type: Boolean,
      required: false,
      default: false
    },
    locale: {
      type: String,
      required: false,
      default: null
    },
    isInitialFocusEnabled: {
      type: Boolean,
      required: false,
      default: false
    }
  },

  data: () => ({
    authInstance: null,
    state: 'loading',
    config: null
  }),

  computed: {
    currentLocale() {
      return this.locale || navigator.language.substring(0, 2)
    }
  },

  created() {
    if (!this.isOdsProvided) {
      // TODO: After we enable importing single components, remove this
      Vue.use(DesignSystem)
    }

    this.initAuthentication()
  },

  mounted() {
    this.$language.current = this.currentLocale
  },

  beforeDestroy() {
    this.authInstance.mgr.events.removeUserLoaded()
  },

  methods: {
    initApp() {
      if (!this.isSdkProvided) {
        const bearerToken = this.bearerToken || this.authInstance.getToken()

        // Init owncloud-sdk
        this.$client.init({
          baseUrl: this.config.server,
          auth: {
            bearer: bearerToken
          },
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })
      }

      this.state = 'authorized'
    },

    async initAuthentication() {
      this.config = await loadConfig(this.configObject, this.configLocation)

      if (this.bearerToken) {
        return this.initApp()
      }

      this.authInstance = initVueAuthenticate(this.config)
      this.checkUserAuthentication()
    },

    checkUserAuthentication() {
      if (this.authInstance.isAuthenticated()) {
        return this.initApp()
      }

      this.state = 'unauthorized'

      // If the user is not authenticated, we add event listener when he logs in to automatically init the application afterwards
      this.authInstance.mgr.events.addUserLoaded(() => {
        this.initApp()
      })
    },

    authenticate() {
      this.authInstance.authenticate()
    },

    selectResources(resources) {
      this.$emit('update', resources)
    },

    emitSelectBtnClick(resources) {
      this.$emit('select', resources)
    },

    cancel() {
      if (this.cancelBtnLabel === null) {
        // don't propagate cancel events if we don't have a cancel button
        return
      }
      this.$emit('cancel')
    },

    onFolderLoaded(folder) {
      this.$emit('folderLoaded', folder)
    }
  }
}
</script>

<style>
/* Import oC CI font and design system styles */
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap');
@import '../node_modules/owncloud-design-system/dist/system/system.css';

* {
  font-family: 'Source Sans Pro', sans-serif;
}
</style>

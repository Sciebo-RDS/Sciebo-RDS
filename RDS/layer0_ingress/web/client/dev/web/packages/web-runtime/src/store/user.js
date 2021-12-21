import initVueAuthenticate from '../services/auth'
import router from '../router/'

import SidebarQuota from '../components/SidebarQuota.vue'

let vueAuthInstance

const state = {
  token: '',
  id: '',
  displayname: null,
  email: null,
  isAuthenticated: false,
  capabilities: [],
  version: {},
  groups: [],
  userReady: false,
  quota: null
}

const actions = {
  cleanUpLoginState(context) {
    if (context.state.id === '') {
      return
    }
    // reset user to default state
    context.commit('SET_USER', state)
    // reset capabilities to default state
    context.commit('SET_CAPABILITIES', { capabilities: null, version: null })
    // set userReady to false
    context.commit('SET_USER_READY', false)

    // clear oidc client state
    vueAuthInstance.clearLoginState()
  },
  async logout({ dispatch }) {
    const logoutFinalizer = (forceRedirect = false) => {
      // Remove signed in user
      dispatch('cleanUpLoginState')
      dispatch('hideModal')
      dispatch('loadSettingsValues')

      // Force redirect to login
      if (forceRedirect) {
        router.push({ name: 'login' })
      }
    }
    const u = await vueAuthInstance.getStoredUserObject()

    if (u && u.id_token) {
      vueAuthInstance
        .createSignoutRequest({ id_token_hint: u.id_token })
        .then(signoutRequestUrl => {
          logoutFinalizer()

          // Navigate to signout URL
          window.open(signoutRequestUrl, '_self')
        })
        .catch(error => {
          console.error(error)
        })
    } else {
      // Oauth2 logout
      logoutFinalizer(true)
    }
  },
  async initAuth(context, payload = { autoRedirect: false }) {
    const init = async (client, token, doLogin = true) => {
      const instance = context.rootState.config.server || window.location.origin
      const options = {
        baseUrl: instance,
        auth: {
          bearer: token
        },
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      }
      if (context.state.id) {
        options.userInfo = {
          id: context.state.id,
          'display-name': context.state.displayname,
          email: context.state.email
        }
      }

      client.init(options)
      if (doLogin) {
        let login
        try {
          login = await client.login()
        } catch (e) {
          console.warn('Seems that your token is invalid. Error:', e)
          context.dispatch('cleanUpLoginState')
          router.push({ name: 'accessDenied' })
          return
        }

        const capabilities = await client.getCapabilities()
        context.commit('SET_CAPABILITIES', capabilities)

        const userGroups = await client.users.getUserGroups(login.id)
        const user = await client.users.getUser(login.id)

        context.commit('SET_USER', {
          id: login.id,
          username: login.username,
          displayname: login.displayname || login['display-name'],
          email: !Object.keys(login.email).length ? '' : login.email,
          token,
          isAuthenticated: true,
          groups: userGroups
        })

        // Display quota in the sidebar
        if (user.quota.definition !== 'default' && user.quota.definition !== 'none') {
          context.commit('SET_QUOTA', user.quota)
          context.commit('SET_SIDEBAR_FOOTER_CONTENT_COMPONENT', SidebarQuota, { root: true })
        } else {
          context.commit('SET_SIDEBAR_FOOTER_CONTENT_COMPONENT', null, { root: true })
        }

        await context.dispatch('loadSettingsValues')
        context.commit('SET_USER_READY', true)

        if (payload.autoRedirect) {
          router.push({ path: '/' }).catch(() => {})
        }
      } else {
        context.commit('UPDATE_TOKEN', token)
      }
    }
    // if called from login, use available vue-authenticate instance; else re-init
    if (!vueAuthInstance) {
      vueAuthInstance = initVueAuthenticate(context.rootState.config)
      const client = this._vm.$client
      vueAuthInstance.events().addAccessTokenExpired(function() {
        console.log('AccessToken Expired：', arguments)
      })
      vueAuthInstance.mgr.events.addAccessTokenExpiring(function() {
        console.log('AccessToken Expiring：', arguments)
      })
      vueAuthInstance.events().addUserLoaded(user => {
        console.log(
          `New User Loaded. access_token： ${user.access_token}, refresh_token: ${user.refresh_token}`
        )
        init(client, user.access_token, false)
      })
      vueAuthInstance.events().addUserUnloaded(() => {
        console.log('user unloaded…')
        context.dispatch('cleanUpLoginState')
        router.push({ name: 'login' })
      })
      vueAuthInstance.events().addSilentRenewError(error => {
        console.error('Silent Renew Error：', error)
        context.dispatch('cleanUpLoginState')
        router.push({ name: 'accessDenied' })
      })
    }
    const token = vueAuthInstance.getToken()
    if (token) {
      await init(this._vm.$client, token)
    }
  },
  login(context, payload = { provider: 'oauth2' }) {
    // reset vue-authenticate
    vueAuthInstance = initVueAuthenticate(context.rootState.config)
    vueAuthInstance.authenticate(payload.provider, {}, {}).then(() => {
      if (vueAuthInstance.isAuthenticated) {
        context.dispatch('initAuth')
      }
    })
  },
  callback(context) {
    if (!vueAuthInstance) vueAuthInstance = initVueAuthenticate(context.rootState.config)
    vueAuthInstance.mgr
      .signinRedirectCallback()
      .then(() => {
        const autoRedirect = true
        context.dispatch('initAuth', { autoRedirect })
      })
      .catch(e => {
        console.warn('error in OpenIdConnect:', e)
        context.dispatch('cleanUpLoginState')
        router.push({ name: 'accessDenied' })
      })
  },
  signinSilentCallback(context) {
    if (!vueAuthInstance) vueAuthInstance = initVueAuthenticate(context.rootState.config)
    vueAuthInstance.mgr.signinSilentCallback().then(() => {
      context.dispatch('initAuth')
    })
  }
}

const mutations = {
  SET_USER(state, user) {
    state.displayname = user.displayname
    state.id = user.id
    state.username = user.username
    state.email = user.email
    state.isAuthenticated = user.isAuthenticated
    state.token = user.token
    state.groups = user.groups
  },
  SET_CAPABILITIES(state, data) {
    state.capabilities = data.capabilities
    state.version = data.version
  },
  UPDATE_TOKEN(state, token) {
    state.token = token
  },
  SET_USER_READY(state, ready) {
    state.userReady = ready
  },

  SET_QUOTA(state, quota) {
    // Turn strings into ints
    quota.free = parseInt(quota.free)
    quota.relative = parseInt(quota.relative)
    quota.used = parseInt(quota.used)
    quota.total = parseInt(quota.total)

    state.quota = quota
  }
}

const getters = {
  isAuthenticated: state => {
    return state.isAuthenticated
  },
  getToken: state => {
    return state.token
  },
  user: state => {
    return state
  },
  capabilities: state => {
    return state.capabilities
  },

  quota: state => state.quota
}

export default {
  state,
  actions,
  mutations,
  getters
}

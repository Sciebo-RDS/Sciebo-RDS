import config from "./config.js"
import store from "./store.js"
import integrations from "./plugins/integration/index.js"
import routes from './router/index.js'
import customMethods from "./plugins/customMethods.js"
import translations from "./translations/index.js"
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from './App.vue'
import Vuex from 'vuex';
import vuetify from './plugins/vuetify.js';

const vuet = vuetify.vuetify

function install(Vue) {
    Vue.use(config)
    Vue.use(Vuex)
    Vue.use(store)
    axios.defaults.withCredentials = true;
    Vue.use(VueAxios, axios)
    Vue.use(vuetify)
    Vue.use(customMethods)
    Vue.use(integrations)
}

export default {
    install,
    App: App,
    routes: routes,
    store: store.store,
    translations: translations,
    vuetify: vuet
}
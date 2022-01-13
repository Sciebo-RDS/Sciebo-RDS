import Vue from 'vue';
import Vuex from 'vuex';
import Settings from "./modules/Settings"
import RDS from "./modules/RDS"
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex)

let plugins = []

if (process.env.NODE_ENV === "production") {
    plugins.push(createPersistedState())
}

const store = new Vuex.Store({
    modules: {
        RDSStore: RDS,
        SettingsStore: Settings
    },
    plugins,
    strict: process.env.NODE_ENV !== 'production'
})

export default store
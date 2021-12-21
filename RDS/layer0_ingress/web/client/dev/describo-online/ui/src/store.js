import { cloneDeep } from "lodash";
import Vue from "vue";
import Vuex from "vuex";
import VuexPersistence from "vuex-persist";
const vuexLocal = new VuexPersistence({
    storage: window.sessionStorage,
    reducer: (state) => {
        let saveState = {
            session: {
                create: state.session.create,
            },
            target: state.target,
        };
        return saveState;
    },
    filter: (mutation) => {
        return ["reset", "setTargetResource", "setActiveCollection"].includes(mutation.type);
    },
});

Vue.use(Vuex);

const mutations = {
    reset: (state) => {
        state = cloneDeep(resetState());
    },
    saveConfiguration: (state, payload) => {
        state.configuration = { ...payload.configuration };
    },
    setTargetResource: (state, payload) => {
        state.session = { create: new Date() };
        state.target = { ...payload };
    },
    setActiveCollection(state, payload) {
        state.collection = { ...payload };
    },
    setSelectedEntity(state, payload) {
        state.selectedEntity = { ...payload };
    },
};

const actions = {
    async loadConfiguration({ commit }) {
        let response = await fetch("/api/configuration");
        if (response.status === 200) {
            let { configuration } = await response.json();
            commit("saveConfiguration", { configuration });
        }
    },
};

export const store = new Vuex.Store({
    state: resetState(),
    mutations,
    actions,
    modules: {},
    plugins: [vuexLocal.plugin],
});

function resetState() {
    return {
        session: {
            create: new Date(),
        },
        configuration: undefined,
        target: {
            resource: undefined,
            folder: undefined,
        },
        collection: {},
        selectedEntity: { id: "RootDataset" },
    };
}

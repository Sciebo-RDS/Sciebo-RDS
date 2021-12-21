const urlParams = new URLSearchParams(window.location.search);

const language = () => {
    const ll_CC = urlParams.get('lang') || navigator.language || navigator.userLanguage;
    return ll_CC.split("-", 1)[0];
}

const getDefaultState = () => {
    return {
        darkMode: false,
        deviceMode: true,
        timeMode: false,
        language: language(),
        finishedWizard: false,
        showAllProjects: false,
        questions: {}
    }
}

export default {
    getDefaultState,
    name: "SettingsStore",
    // You can use it as state property
    state: getDefaultState(),

    // You can use it as a state getter function (probably the best solution)
    getters: {
        getLanguage(state) {
            return urlParams.get('lang') || state.language;
        },
        getQuestions(state) {
            return state.questions
        },
        isDarkMode(state) {
            if (state.deviceMode) {
                return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            }
            if (state.timeMode) {
                const today = new Date();
                return today.getHours() < 8 || today.getHours() > 20;
            }
            return state.darkMode == true
        },
        usingDeviceMode(state) {
            return state.deviceMode == true
        },
        usingDarkMode(state) {
            return state.darkMode == true
        },
        usingTimeMode(state) {
            return state.timeMode == true
        },
        isWizardFinished(state) {
            return state.finishedWizard
        },
        showAllProjects(state) {
            return state.showAllProjects
        }
    },

    // Mutation for when you use it as state property
    mutations: {
        resetState(state) {
            // Merge rather than replace so we don't lose observers
            // https://github.com/vuejs/vuex/issues/1118
            Object.assign(state, getDefaultState())
        },
        setLanguage(state, payload) {
            state.language = payload.language
        },
        setDarkMode(state, payload) {
            state.darkMode = payload.darkMode
        },
        setQuestions(state, payload) {
            state.questions = payload.questions
        },
        setDeviceMode(state, payload) {
            state.deviceMode = payload.deviceMode
        },
        setTimeMode(state, payload) {
            state.timeMode = payload.timeMode
        },
        setWizardFinished(state, payload) {
            if (!!payload) {
                state.finishedWizard = payload.wizard
            } else {
                state.finishedWizard = true
            }
        },
        showAllProjects(state, payload) {
            state.showAllProjects = payload;
        }
    },
    actions: {
        setLanguage(context, state) {
            context.commit('setLanguage', {
                language: state.language
            })
        },
        setDarkMode(context, state) {
            context.commit('setDarkMode', {
                darkMode: state.darkMode
            })
        },
        setQuestions(context, state) {
            context.commit('setQuestions', {
                questions: state.questions
            })
        },
        setDeviceMode(context, state) {
            context.commit('setDeviceMode', {
                deviceMode: state.deviceMode
            })
        },
        setTimeMode(context, state) {
            context.commit('setTimeMode', {
                timeMode: state.timeMode
            })
        }
    }
};
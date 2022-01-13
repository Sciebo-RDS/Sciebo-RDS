const config = {
    productionTip: false,
    socket: {
        server: process.env.SOCKETIO_HOST || "$SOCKETIO_HOST",
        path: process.env.SOCKETIO_PATH || "$SOCKETIO_PATH"
    },
    server: process.env.VUE_APP_FRONTENDHOST || "$VUE_APP_FRONTENDHOST",
    describo: process.env.VUE_APP_DESCRIBO_URL || "$VUE_APP_DESCRIBO_URL",
    predefined_user: (process.env.DEV_USE_PREDEFINED_USER === "True")
}

export default {
    config,
    install: function (Vue) {
        for (const [key, value] of Object.entries(config)) {
            Vue.config[key] = value
        }
        Vue.prototype.$config = Vue.config
    }
}
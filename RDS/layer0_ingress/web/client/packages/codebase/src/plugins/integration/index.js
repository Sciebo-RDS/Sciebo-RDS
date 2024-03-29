import standalone from "./standalone";
import embed from "./embed.js"

export default {
    install(Vue) {
        Vue.prototype.auth = {}
        Vue.prototype.auth.loginMethods = []
        Vue.prototype.auth.prelogin = []
        Vue.prototype.auth.isLoading = true

        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('embed')) {
            Vue.use(embed)
        } else {
            Vue.use(standalone)
        }

        Vue.prototype.auth.loggedIn = false

        function loggedIn() {
            Vue.prototype.auth.loggedIn = true
            Vue.prototype.$socket.client.on('connect', disableLoadingIndicator);
            Vue.prototype.$socket.client.open()
        }

        function disableLoadingIndicator() {
            Vue.prototype.auth.isLoading = false
            Vue.prototype.$socket.client.off('connect', disableLoadingIndicator);
        }

        Vue.prototype.auth.login = function () {
            // First check, if we have already a session
            Vue.prototype.$http.get(`${Vue.config.server}/login`).then(() => {
                loggedIn();
            }).catch((resp) => {
                //if not, execute all loginMethods
                Vue.prototype.auth.loggedIn = false;
                Promise.all(Vue.prototype.auth.loginMethods.map((fn) => fn())).then((results) => {
                    if (results.includes(true)) {
                        loggedIn();
                    }
                })
            })
        }
    }
}
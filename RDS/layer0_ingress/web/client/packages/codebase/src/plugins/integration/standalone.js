export default {
    install(Vue) {
        Vue.prototype.auth.loginMethods.push(() => {
            return new Promise((resolve, reject) => {
                const urlParams = new URLSearchParams(window.location.search);
                const token = urlParams.get("access_token")
                const state = urlParams.get("state")

                if (token !== undefined) {
                    Vue.prototype.$http.post(`${Vue.config.server}/login`, { access_token: token, state: state }).then((resp) => {
                        resolve(true)
                    }).catch(() => {
                        resolve(false)
                    })
                }
                return false
            })
        })

        Vue.prototype.showFilePicker = function (projectId) {
            // TODO: Show the filePicker component in overlay or sth. Vue events maybe?
            // Can we find a solution, where this approach does not appear in embed version?
        }
    }
}
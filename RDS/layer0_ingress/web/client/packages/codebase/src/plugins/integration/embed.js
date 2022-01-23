import store from "store"

export default {
    install(Vue) {
        let parWindow = window.parent;

        let initProm = new Promise(function (resolve, reject) {
            let timer = setInterval(function () {
                clearInterval(timer)
                reject(new Error('no value through response'))
            }, 10000)

            window.addEventListener("message", (event) => {
                if (event.data.length > 0) {
                    var payload = JSON.parse(event.data);
                    switch (payload.event) {
                        case "informations":
                            let parsed = JSON.parse(payload.data)
                            let info = parsed.jwt

                            store.commit("setOwnCloudServername", parsed.serverName)

                            Vue.prototype.$http.post(`${Vue.config.server}/login`, { informations: info }).then(
                                (resp) => {
                                    clearInterval(timer)
                                    resolve(resp)
                                },
                                (resp) => {
                                    clearInterval(timer)
                                    reject(resp)
                                })
                            break;
                    }
                }
            });
        })

        Vue.prototype.auth.loginMethods.push(() => {
            return new Promise((resolve, reject) => {
                parWindow.postMessage(JSON.stringify({
                    event: "init"
                }), "*")

                initProm.then(() => {
                    resolve(true)
                }).catch(() => {
                    resolve(false)
                })
            })
        })

        Vue.prototype.showFilePicker = function (projectId, location) {
            parWindow.postMessage(JSON.stringify({
                event: "showFilePicker",
                data: {
                    projectId: projectId,
                    filePath: location
                }
            }), "*")
        }
    }
}
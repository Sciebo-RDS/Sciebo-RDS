import "regenerator-runtime";
import "@/assets/tailwind.css";
import "element-ui/lib/theme-chalk/index.css";
import "@fortawesome/fontawesome-free/js/all";
import { config } from "@fortawesome/fontawesome-svg-core";
config.autoReplaceSvg = "nest";

import Vue from "vue";
import App from "./App.vue";
import router from "./routes";
import { store } from "./store";
import ElementUI from "element-ui";
import locale from "element-ui/lib/locale/lang/en";
import OktaPlugin from "./plugins/okta";
import OneDrivePlugin from "./plugins/onedrive";
import OwncloudPlugin from "./plugins/owncloud";
import log from "loglevel";
import prefix from "loglevel-plugin-prefix";
const level = process.env.NODE_ENV === "development" ? "debug" : "warn";
log.setLevel(level);
const prefixer = prefix.noConflict();
prefixer.reg(log);
prefixer.apply(log);
import { io } from "socket.io-client";
import HTTPService from "./components/http.service";

(async () => {
    let response = await fetch("/api/configuration");
    if (response.status === 200) {
        let { configuration } = await response.json();

        Vue.prototype.$http = new HTTPService({ $auth: Vue.prototype.$auth });
        Vue.prototype.$log = log;
        Vue.prototype.$socket = io();

        Vue.use(ElementUI, { locale });

        // enable defined components
        enableOkta({ Vue, log, router, configuration });
        enableOnedrive({ Vue, log, configuration });
        enableOwncloud({ Vue, log, router, configuration });

        store.commit("saveConfiguration", { configuration });
        Vue.config.productionTip = false;

        new Vue({
            router,
            store,
            render: (h) => h(App),
        }).$mount("#app");
    }
})();

function enableOkta({ Vue, log, router, configuration }) {
    if (configuration.services.okta) {
        Vue.use(OktaPlugin, {
            ...configuration.services.okta,
            log,
            router,
        });
    }
}

function enableOnedrive({ Vue, log, configuration }) {
    if (configuration.services.onedrive) {
        Vue.use(OneDrivePlugin, {
            ...configuration.services.onedrive,
            log,
            $http: Vue.prototype.$http,
            configuration: "/session/configuration/onedrive",
        });
    }
}

function enableOwncloud({ Vue, log, router, configuration }) {
    if (configuration.services.owncloud) {
        Vue.use(OwncloudPlugin, {
            router,
            log,
            $http: Vue.prototype.$http,
            configuration: "/session/configuration/owncloud",
            oauthToken: "/session/get-oauth-token/owncloud",
        });
    }
}

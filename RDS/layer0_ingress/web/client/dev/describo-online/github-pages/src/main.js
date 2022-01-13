import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import "./assets/index.css";
import fontawesome from "@fortawesome/fontawesome-free/js/all";
import { config } from "@fortawesome/fontawesome-svg-core";
config.autoReplaceSvg = "nest";

Vue.config.productionTip = false;

new Vue({
    router,
    render: (h) => h(App),
}).$mount("#app");

import Vue from 'vue'
import App from "./App.vue"
import DesignSystem from 'owncloud-design-system'

Vue.use(DesignSystem)

new Vue({
    render: h => h(App)
}).$mount('#app')

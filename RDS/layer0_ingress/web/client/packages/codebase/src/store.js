import store from './store/index.js'
export default {
    store,
    install(Vue) {
        Vue.prototype.$store = store
    }
}
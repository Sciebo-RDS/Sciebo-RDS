import Vuetify from 'vuetify';
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/dist/vuetify.min.css';
import colors from 'vuetify/lib/util/colors'

export default {
    install(Vue) {
        Vue.use(Vuetify);
    },
    vuetify: new Vuetify({
        icons: {
            iconfont: 'mdi',
        },
        theme: {
            themes: {
                light: {sidebar : '#f5f5f5', 'sidebar-selected': '#006064'},
                dark: {}
            },
        }
    })
};

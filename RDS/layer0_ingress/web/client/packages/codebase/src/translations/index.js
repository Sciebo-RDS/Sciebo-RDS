import GetTextPlugin from 'vue-gettext'
import translations from './translations.json'

export default {
    install(Vue) {
        Vue.use(GetTextPlugin, {
            availableLanguages: {
                en: 'English',
                de: 'Deutsch'
            },
            defaultLanguage: 'en',
            translations: translations,
            silent: true
        })
    }
}
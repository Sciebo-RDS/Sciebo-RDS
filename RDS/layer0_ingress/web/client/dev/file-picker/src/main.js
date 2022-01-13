import Vue from './vue'
import App from './App.vue'

new Vue({
  render: (h) => {
    return h(App, {
      props: {
        variation: 'resource'
      }
    })
  }
}).$mount('#app')

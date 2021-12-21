<template>
  <div
    class="uk-height-1-1 uk-width-1-1 uk-flex uk-flex-middle uk-flex-center"
    :style="{ backgroundImage: 'url(' + backgroundImage + ')' }"
  >
    <div class="oc-login-card">
      <div class="oc-login-card-body">
        <h3 class="oc-login-card-title" v-text="$gettext('Welcome to ownCloud File picker')" />
        <p
          v-text="
            $gettext('Please, click the button below to authenticate and get access to your data.')
          "
        />
        <oc-button variation="primary" @click="login" v-text="$gettext('Log in')" />
      </div>
    </div>
  </div>
</template>

<script>
import backgroundImage from '../assets/img/background.jpg'

export default {
  name: 'Login',

  computed: {
    backgroundImage() {
      return backgroundImage
    }
  },

  methods: {
    login() {
      this.$emit('login')
    }
  }
}
</script>

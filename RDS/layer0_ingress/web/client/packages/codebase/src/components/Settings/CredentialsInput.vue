<template>
  <v-card>
    <v-card-title class="headline">
      <translate>Add service</translate>
    </v-card-title>

    <v-card-text>
      <div v-show="noInput">
        <translate>
          This service does not require any input, as it can derive the credentials by other means.
        </translate>
      </div>
      <div v-show="!noInput">
        <translate>
          Enter your credentials for %{ parsedServicename }.
        </translate>
      </div>

      <v-text-field
        v-if="showUsername"
        v-model="username"
        :rules="rules"
        :label="$gettext(`Username`)"
        @keydown.enter="saveCredentials"
      ></v-text-field>
      <v-text-field
        ref="passwordInput"
        v-if="showPassword"
        v-model="password"
        :rules="rules"
        :label="$gettext(`Password`)"
        :append-icon="passwordShow ? 'mdi-eye' : 'mdi-eye-off'"
        :type="passwordShow ? 'text' : 'password'"
        @click:append="passwordShow = !passwordShow"
        @keydown.enter="saveCredentials"
      >
      </v-text-field>
    </v-card-text>
    <v-divider></v-divider>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn @click="saveCredentials" color="primary" v-trans>
        <translate>Save credentials</translate>
      </v-btn>
      <v-btn @click="$emit('closecredentials')" color="error">
        <translate>Cancel input</translate>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    showUsername: Boolean,
    showPassword: Boolean,
    servicename: String,
    visible: Boolean,
  },
  data: () => ({
    rules: [
      (value) => !!value || "Required.",
      (value) => (value && value.length >= 3) || "Min 3 characters",
    ],
    username: "",
    password: "",
    passwordShow: false,
  }),
  computed: {
    parsedServicename() {
      return this.parseServicename(this.servicename);
    },
    noInput() {
      return !this.showUsername && !this.showPassword;
    },
  },
  methods: {
    checkInputs() {
      if (!this.showUsername && !this.showPassword) {
        this.saveCredentials();
      }
    },
    saveCredentials() {
      this.$store.dispatch("addServiceWithCredentials", {
        username: this.username,
        password: this.password,
        servicename: this.servicename,
      });
      this.$emit("closecredentials");
    },
  },
};
</script>
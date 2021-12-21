<template>
  <v-card class="mx-auto pa-4" min-width="300px">
    <v-card-title v-translate>Settings for theme</v-card-title>
    <v-switch
      flat
      v-model="deviceMode"
      :label="$gettext('Using DeviceMode?')"
    ></v-switch>
    <v-switch
      flat
      v-model="darkMode"
      :label="$gettext('Enable DarkMode?')"
      :disabled="deviceMode == true"
    ></v-switch>
  </v-card>
</template>

<script>
export default {
  name: "ThemeSelector",
  computed: {
    darkMode: {
      get() {
        return this.$store.getters.isDarkMode;
      },
      set(value) {
        this.$vuetify.theme.dark = value;
        this.$store.dispatch("setDarkMode", { darkMode: value });
      },
    },
    deviceMode: {
      get() {
        return this.$store.getters.usingDeviceMode;
      },
      set(value) {
        this.$store.dispatch("setDeviceMode", { deviceMode: value });
      },
    },
  },
  watch: {
    darkMode(newVal) {
      this.$vuetify.theme.dark = newVal;
    },
  },
};
</script>
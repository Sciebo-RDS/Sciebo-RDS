<template>
  <v-menu
    :top="!$vuetify.breakpoint.mobile"
    offset-y
    :close-on-content-click="false"
    :close-on-click="false"
    dark
    max-width="280px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-list class="d-none d-lg-flex">
        <v-list-item-group style="position: fixed; bottom:0px; width:100%;">
          <v-list-item v-bind="attrs" v-on="on">
            <v-list-item-icon>
              <v-icon>mdi-cog</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="$gettext('Settings')" />
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>

      <v-btn icon v-bind="attrs" v-on="on" class="d-lg-none">
        <v-icon>mdi-cog</v-icon>
      </v-btn>
    </template>

    <v-card>
      <v-container fluid>
        <v-subheader>{{ $gettext("Theme") }}</v-subheader>
        <v-btn
          v-for="item in modes"
          :key="item.text"
          @click="item.click"
          class="ma-1"
          style="width:120px"
          :color="item.active() ? 'primary' : ''"
        >
          {{ item.text }} <v-icon right>{{ item.icon }}</v-icon>
        </v-btn>
        <div v-if="!languagePredefined">
          <v-subheader>{{ $gettext("Language") }}</v-subheader>
          <v-btn
            v-for="item in availableLanguages"
            :key="item.short"
            class="ma-1"
            style="width:120px"
            :color="item.short == language.short ? 'primary' : ''"
            @click="language = item.short"
          >
            {{ item.long }}
          </v-btn>
        </div>
        <div style="width: 100%; text-align:center;">
          <v-btn
            x-small
            depressed
            plain
            color="error"
            class="mt-3 mb-1"
            @click="$router.push('/removeRDS')"
          >
            <translate>Remove account</translate>
          </v-btn>
        </div>
      </v-container>
    </v-card>
  </v-menu>
</template>

<script>
export default {
  data() {
    return {
      modes: [
        {
          text: "Light",
          icon: "mdi-white-balance-sunny",
          click: () => {
            this.deviceMode = false;
            this.darkMode = false;
            this.timeMode = false;
          },
          active: () => {
            return !this.darkMode && !this.deviceMode && !this.timeMode;
          },
        },
        {
          text: "Dark",
          icon: "mdi-weather-night",
          click: () => {
            this.deviceMode = false;
            this.timeMode = false;
            this.darkMode = true;
          },
          active: () => {
            return this.darkMode && !this.deviceMode && !this.timeMode;
          },
        },
        {
          text: "System",
          icon: "mdi-desktop-classic",
          click: () => {
            this.timeMode = false;
            this.deviceMode = true;
          },
          active: () => {
            return this.deviceMode;
          },
        },
        {
          text: "Mixed",
          icon: "mdi-theme-light-dark",
          click: () => {
            this.deviceMode = false;
            this.timeMode = true;
            this.startTimeMode();
          },
          active: () => {
            return this.timeMode;
          },
        },
      ],
    };
  },
  computed: {
    availableLanguages: function() {
      console.log(this.$vuetify.theme.themes);
      let res = [];
      for (const [key, value] of Object.entries(this.$language.available)) {
        res.push({ short: key, long: value });
      }

      return res;
    },
    language: {
      set(value) {
        this.$config.language = value;
        this.$store.dispatch("setLanguage", { language: value });
      },
      get() {
        return {
          short: this.$store.getters.getLanguage,
          long: this.$language.available[this.$store.getters.getLanguage],
        };
      },
    },
    languagePredefined() {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.has("lang");
    },
    darkMode: {
      get() {
        return this.$store.getters.usingDarkMode;
      },
      set(value) {
        this.$store.dispatch("setDarkMode", { darkMode: value });
        this.$vuetify.theme.dark = this.$store.getters.isDarkMode;
      },
    },
    deviceMode: {
      get() {
        return this.$store.getters.usingDeviceMode;
      },
      set(value) {
        this.$store.dispatch("setDeviceMode", { deviceMode: value });
        this.$vuetify.theme.dark = this.$store.getters.isDarkMode;
      },
    },
    timeMode: {
      get() {
        return this.$store.getters.usingTimeMode;
      },
      set(value) {
        this.$store.dispatch("setTimeMode", { timeMode: value });
        this.$vuetify.theme.dark = this.$store.getters.isDarkMode;
      },
    },
  },
  watch: {
    darkMode(newVal) {
      this.$vuetify.theme.dark = newVal;
    },
  },
  methods: {
    console(val) {
      console.log(val);
    },
    loopTimeMode() {
      if (this.timeMode) {
        const today = new Date();
        this.darkMode = today.getHours() < 8 || today.getHours() > 20;
      }
    },
    startTimeMode() {
      this.loopTimeMode();
      let timer = setInterval(() => {
        if (!this.timeMode) {
          clearInterval(timer);
        }
        this.loopTimeMode();
      }, 1000 * 60 * 5);
    },
  },
  beforeMount() {
    this.startTimeMode();
  },
};
</script>

<style></style>

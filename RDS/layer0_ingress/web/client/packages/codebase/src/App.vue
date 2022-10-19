<template>
  <div>
    <v-app id="inspire">
      <!-- pilot warning bar -->
      <v-system-bar
      color="warning" absolute height="25px">
        <v-row class="font-weight-bold" justify="center" >
          <v-icon>
            mdi-comment-alert-outline
          </v-icon>
          RDS is still in its pilot phase. If you encounter any problems, please contact
          <a :href="`mailto:${$store.getters.getSupportEmail}`" class="ml-1 black--text">{{ $store.getters.getSupportEmail }}</a>.
        </v-row>
      </v-system-bar>

      <!-- Bar without warning / message -->
      <!-- <v-system-bar
        color="success"
        absolute
        height="25px"/> -->

      <overlay :subtext="overlayText" />
      <snackbar />
      <v-app-bar v-if="$vuetify.breakpoint.mobile" app flat class="d-lg-none">
        <v-app-bar-nav-icon @click="drawer = !drawer" class="d-lg-none" />
        <v-spacer />
        <settingsmenu />
      </v-app-bar>

      <v-navigation-drawer
        v-if="$store.getters.isWizardFinished"
        id="v-navigation-drawer"
        v-model="drawer"
        app
        bottom
        color="sidebar"
      >

            <v-row no-gutters class="text-center pt-6 pb-5">
              <v-col>
                <v-avatar class="mb-5" size="5em">
                  <v-img :src="$vuetify.theme.dark ? require('./assets/RDS_Logo_Weiss.svg') : require('./assets/RDS_Logo_Schwarz.svg')" />
                </v-avatar>
              </v-col>
              <v-col cols="12">
                <div
                  :class="[
                    'text-h6',
                    $socket.connected ? 'primary--text' : 'error--text',
                  ]"
                  v-text="'Sciebo RDS'"
                />
              </v-col>
            </v-row>


        <v-list
          class="d-flex flex-column mb-10 mt-5">
          <v-list-item-group v-model="model" mandatory color="sidebar-selected">
            <v-list-item
              v-for="(item, i) in views"
              :key="i"
              :to="item.path"
              v-ripple="false"
              v-show="
                !$store.getters.isWizardFinished != !item.hide ||
                  item.name == 'Home'
              "
            >
              <v-list-item-icon>
                <v-icon v-text="item.icon" />
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title v-text="$gettext(item.title)" />
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
        <settingsmenu
          v-if="!$vuetify.breakpoint.mobile"
          class="d-none d-lg-flex"
        />
      </v-navigation-drawer>

      <v-main class="ml-0 mb-0">
        <v-container
            fluid
            class="pb-0 px-0 mb-0 mr-0">
                <router-view />
        </v-container>
      </v-main>
    </v-app>
  </div>
</template>

<style lang="scss" scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.v-list-item {
  flex: 0;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>

<script>
import { mapGetters } from "vuex";
import overlay from "./components/Overlay.vue";
import settingsmenu from "./components/Menu/Settings.vue";
import snackbar from "./components/Snackbar.vue";

export default {
  name: "App",
  props: {
    server: { type: String, default: null },
  },
  sockets: {
    connect: function() {
      console.log("socket connected");
    },
    disconnect() {
      this.isConnected = false;
      console.log("server disconnected");
    },
  },
  data() {
    return {
      drawer: null,
      model: null,
      overlayText: null,
    };
  },
  components: { overlay, settingsmenu, snackbar },
  methods: {},
  computed: {
    ...mapGetters({
      isDarkMode: "isDarkMode",
      getLanguage: "getLanguage",
    }),
    views() {
      return this.$router.options.routes;
    },
  },
  beforeCreate() {
    this.auth.login();
    const routeName = "Wizard";

    if (
      !this.$store.getters.isWizardFinished &&
      this.$route.name !== routeName
    ) {
      this.$router.push({ name: routeName });
    }
  },
  beforeMount() {
    this.overlayText = this.$gettext("initialization...");

    this.$root.$emit("showoverlay");
    var checkLoginStatus = setInterval(() => {
      this.$root.$emit("showoverlay");
      if (!this.auth.isLoading) {
        clearInterval(checkLoginStatus);
        this.overlayText = undefined;
        this.$root.$emit("hideoverlay");
      }
    }, 500);
    this.$config.language = this.getLanguage;

    this.$vuetify.theme.dark = this.$store.getters.isDarkMode;

    Vue.prototype.$http
      .get(`${Vue.config.server}/faq`)
      .then((response) => {
        this.$store.commit("setQuestions", {
          questions: response.data,
        });
      })
      .catch(() => {});
  },
};
</script>

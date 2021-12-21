<template>
  <div class="help">
    <Frame :source="'/frames/' + $config.language + '/removal.html'">
      <translate>
        Confirm the checkbox and click the button to remove the RDS account.
      </translate>

      <v-card flat class="d-flex flex-wrap justify-center">
        <v-checkbox
          v-model="checked"
          :label="
            $gettext('Yes, i confirm that i want to delete my RDS account.')
          "
        />
      </v-card>
      <v-card flat class="d-flex flex-wrap justify-center">
        <v-btn @click="uninstallRDS" :disabled="!checked" color="error">
          <translate>Delete RDS account</translate>
        </v-btn>
      </v-card>
    </Frame>
  </div>
</template>

<script>
// @ is an alias to /src
import Frame from "../components/Frame.vue";

export default {
  name: "Help",
  components: {
    Frame,
  },
  data() {
    return {
      checked: false,
      gettingStarted: "https://localhost:8000",
    };
  },
  methods: {
    uninstallRDS() {
      this.$store.dispatch(
        "removeService",
        this.getInformations(
          "port-owncloud",
          this.$store.getters.getUserServiceList
        )
      );
      this.$store.commit("resetState");
      this.$socket.client.close();
      this.auth.loggedIn = false;
      this.auth.isLoading = false;

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

      this.auth.login();
      this.$store.dispatch("getServicesList");
      this.$store.commit("setWizardFinished", { wizard: false });
      this.$router.push({ name: "Wizard" });
    },
  },
};
</script>

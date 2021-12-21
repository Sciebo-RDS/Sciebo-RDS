<template>
  <v-container fluid>
    <Frame
      :source="'/frames/' + $config.language + '/start.html'"
      v-if="!clickedStarted"
      class="fill-height"
    >
      <translate>Click here to</translate>&nbsp;
      <v-btn color="primary" @click="clickGettingStarted">
        <translate>Getting started</translate>
      </v-btn>
    </Frame>
    <v-stepper v-model="currentStep" v-else>
      <v-stepper-header>
        <v-stepper-step :complete="currentStep > 1" step="1">
          <translate>Activate RDS</translate>
        </v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step :complete="currentStep > 2" step="2">
          <translate>Add services</translate>
        </v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step step="3">
          <translate>Finish</translate>
        </v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1">
          <v-card class="mb-12 pa-2" min-height="200px">
            <translate>Permit RDS to access your ownCloud files.</translate>
          </v-card>
          <v-btn
            @click="grantAccess(getInformations('port-owncloud'))"
            color="primary"
            :disabled="!auth.loggedIn"
          >
            <translate>Grant access</translate>
          </v-btn>
        </v-stepper-content>

        <v-stepper-content step="2">
          <v-container flex>
            <v-row justify="start">
              <v-col v-for="(service, index) in filteredServices" :key="index">
                <v-card class="mb-12 pa-2" max-width="500">
                  <v-container>
                    <v-row>
                      <v-col>
                        <translate
                          :translate-params="{
                            name: parseServicename(service.servicename),
                          }"
                        >
                          Connect your %{name} account with RDS
                        </translate>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <v-btn color="primary" @click="grantAccess(service)">
                          <translate>Grant access</translate>
                        </v-btn>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card>
              </v-col>
            </v-row>
          </v-container>

          <v-btn
            color="primary"
            @click="$store.commit('setWizardFinished')"
            :disabled="userservicelist.length == 0"
          >
            <translate>Continue</translate>
          </v-btn>
        </v-stepper-content>

        <v-stepper-content step="3">
          <v-card class="mb-12 pa-2" min-height="200px">
            <translate>You configure RDS properly.</translate>
          </v-card>

          <v-btn color="primary" @click="finishWizard">
            <translate>Go to projects</translate>
          </v-btn>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
    <v-dialog
      v-model="overlay"
      persistent
      max-width="500px"
      :z-index="zIndex"
      @keydown.esc="overlay = false"
    >
      <v-card shaped outlined raised>
        <CredentialsInput
          ref="credinput"
          :showUsername="username"
          :showPassword="password"
          :servicename="servicename"
          v-on:closecredentials="overlay = false"
        />
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import CredentialsInput from "../components/Settings/CredentialsInput.vue";
import Frame from "../components/Frame.vue";

export default {
  data: () => ({
    popup: undefined,
    overlay: false,
    username: "",
    password: "",
    servicename: "",
    zIndex: 1000,
    clickedStarted: false,
    sourceRef: "https://www.research-data-services.de",
  }),
  mounted() {
    if (
      this.$config.predefined_user ||
      this.getInformations("port-owncloud", this.userservicelist) !== undefined
    ) {
      this.finishWizard();
    }

    let timer = setInterval(() => {
      if (
        this.getInformations("port-owncloud", this.userservicelist) !==
        undefined
      ) {
        console.log("found ownCloud in storage");
        clearInterval(timer);
        this.finishWizard();
      }
    }, 1000);
  },
  computed: {
    ...mapState({
      userservicelist: (state) => state.RDSStore.userservicelist,
      servicelist: (state) => state.RDSStore.servicelist,
    }),
    filteredServices() {
      return this.excludeServices(this.servicelist, this.userservicelist);
    },
    currentStep() {
      if (this.$store.getters.isWizardFinished) {
        return 3;
      } else if (
        this.getInformations("port-owncloud", this.userservicelist) !==
        undefined
      ) {
        return 2;
      }
      return 1;
    },
  },
  methods: {
    clickGettingStarted() {
      console.log(process.env);
      if (process.env.NODE_ENV === "development" && this.currentStep > 1) {
        this.clickedStarted = true;
      } else {
        this.grantAccess(this.getInformations("port-owncloud"));
      }
    },
    grantAccess(service) {
      if (!service.credentials) {
        this.openPopup(service, this);
      } else {
        this.servicename = service.servicename;
        this.username = service.credentials.userId;
        this.password = service.credentials.password;
        this.overlay = true;
      }
    },
    finishWizard(path = undefined) {
      this.$store.commit("setWizardFinished");
      if (path == undefined) {
        path = "/";
      }
      this.$router.push(path);
    },
  },
  components: { CredentialsInput, Frame },
};
</script>

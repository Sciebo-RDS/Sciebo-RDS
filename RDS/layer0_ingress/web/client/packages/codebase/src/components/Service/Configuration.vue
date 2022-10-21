<template>
  <v-container>
    <v-row>
      <v-col xl="2" lg="3" md="3" sm="3" xs="12">
        <img contain :src="service.icon" alt="img" style="width: 100%; object-fit: cover; background-color: #ccc;" class="pa-5 rounded-xl" />
        
      </v-col>
      <v-col>
        <v-card flat>
          <v-card-title class="pt-0 pb-5 text-h5">{{ service.displayName }}</v-card-title>
          <v-card-subtitle v-show="!!service.infoUrl || !!service.helpUrl">
            <a
              :href="decodeURIComponent(service.infoUrl)"
              target="_blank"
              class="text-decoration-none"
              v-show="!!service.infoUrl"
            >
              <translate>
                Website
              </translate>
            </a>
            <v-spacer v-show="!!service.infoUrl && !!service.helpUrl" />
            <a
              :href="decodeURIComponent(service.helpUrl)"
              target="_blank"
              class="text-decoration-none"
              v-show="!!service.helpUrl"
            >
              <translate>
                Help
              </translate>
            </a>
          </v-card-subtitle>
          <v-card-text style="white-space: pre-line;">
            {{ service.description[this.$config.language] }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
     <v-card-actions>
            <v-col class="text-right">
              <v-btn
                @click="removeAccess(service)"
                color="warning"
                v-if="userUses(service)"
              >
                <v-icon class="mr-2">mdi-link-variant-off</v-icon>
                <translate
                  key="fae8840f-6d5c-48bf-b8de-860c686cc089"
                  class="mr-1"
                >
                  Disconnect
                </translate>
                {{ service.name }}
              </v-btn>
              <v-btn @click="grantAccess(service)" color="primary" v-else>
                <v-icon class="mr-2">mdi-link-variant</v-icon>
                <translate
                  key="aa3413aa-a9c7-495d-b022-66c7923c67a5"
                  class="mr-1"
                >
                  Connect
                </translate>
                {{ service.name }}
              </v-btn>
            </v-col>
          </v-card-actions>
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
import CredentialsInput from "../Settings/CredentialsInput.vue";

export default {
  props: ["service"],
  components: { CredentialsInput },
  computed: {
    ...mapState({
      userservicelist: (state) => state.RDSStore.userservicelist,
    }),
  },
  data() {
    return {
      overlay: false,
      username: "",
      password: "",
      servicename: "",
    };
  },
  methods: {
    userUses(service) {
      for (var i of this.userservicelist) {
        if (i.servicename === service.servicename) {
          return true;
        }
      }
      return false;
    },
    decodeURIComponent(url) {
      return decodeURIComponent(url);
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
    removeAccess(service) {
      this.$store.dispatch("removeService", service);
    },
  },
};
</script>

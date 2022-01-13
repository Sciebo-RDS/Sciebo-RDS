<template>
  <v-card class="mb-12 pa-2" max-width="500" outlined>
    <v-card-title class="headline">
      {{ parseServicename(service.servicename) }}
    </v-card-title>
    <v-card-text v-if="!remove">
      <translate
        :translate-params="{
          name: parseServicename(service.servicename),
        }"
      >
        Connect your %{name} account with RDS
      </translate>
    </v-card-text>
    <v-card-text v-else>
      <translate
        :translate-params="{
          name: parseServicename(service.servicename),
        }"
      >
        Delete %{name} from your account.
      </translate>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-dialog v-model="dialog" max-width="500px">
        <template v-slot:activator="{ on, attrs }">
          <div>
            <v-btn v-if="!remove" color="primary" @click="grantAccess(service)">
              <translate>Grant access</translate>
            </v-btn>
            <v-btn v-else depressed v-bind="attrs" v-on="on" color="error">
              <translate>Remove access</translate>
            </v-btn>
            <div style="position: relative">
              <translate
                class="float-right"
                tag="small"
                v-if="isOauth(service)"
              >
                (opens a new window)
              </translate>
            </div>
          </div>
        </template>
        <v-card v-if="!remove" shaped outlined raised>
          <CredentialsInput
            ref="credinput"
            :showUsername="username"
            :showPassword="password"
            :servicename="servicename"
            :visible="dialog"
            v-on:closecredentials="dialog = false"
          />
        </v-card>
        <v-card v-else>
          <v-card-title class="headline">
            <translate>Remove service</translate>
          </v-card-title>

          <v-card-text>
            <translate
              tag="p"
              :translate-params="{
                servicename: parseServicename(service.servicename),
              }"
            >
              This will remove your access to %{ servicename } from RDS.
            </translate>
            <translate tag="p">
              If you want to reuse this service, you need to add it again.
            </translate>
            <translate tag="p"> Are you sure? </translate>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              :color="primaryColor"
              text
              @click="
                removeAccess(service);
                dialog = false;
              "
            >
              <translate
                :translate-params="{
                  name: parseServicename(service.servicename),
                }"
              >
                Remove %{ name }
              </translate>
            </v-btn>
            <v-btn :color="errorColor" @click="dialog = false">
              <translate>Cancel</translate>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card-actions>
  </v-card>
</template>

<script>
import CredentialsInput from "../Settings/CredentialsInput.vue";

export default {
  components: { CredentialsInput },
  props: {
    service: Object,
    remove: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    primaryColor() {
      return !this.remove ? "primary" : "error";
    },
    errorColor() {
      return this.remove ? "primary" : "error";
    },
  },
  data: () => ({
    username: "",
    password: "",
    servicename: "",
    dialog: false,
  }),
  methods: {
    isOauth(service) {
      return !service.credentials;
    },
    grantAccess(service) {
      if (this.isOauth(service)) {
        this.openPopup(service, this);
      } else {
        this.servicename = service.servicename;
        this.username = service.credentials.userId;
        this.password = service.credentials.password;
        this.dialog = true;
      }
    },
    removeAccess(service) {
      this.$store.dispatch("removeService", service);
    },
  },
};
</script>

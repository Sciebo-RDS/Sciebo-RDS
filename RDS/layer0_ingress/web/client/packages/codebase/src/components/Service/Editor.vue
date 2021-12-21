<template>
  <div>
    <v-card>
      <v-card-title v-translate>Manage your access to services</v-card-title>
      <v-card-text>
        <v-card flat>
          <v-card-text>
            <translate tag="p">
              In this card, you manage your access to services via RDS.
            </translate>
          </v-card-text>
          <v-divider></v-divider>
        </v-card>
        <v-container flex>
          <v-row justify="start">
            <v-col
              v-for="(service, index) in filteredServices"
              :key="`s` + index"
            >
              <ServiceCard :service="service" :remove="false" />
            </v-col>
            <v-col
              v-for="(service, index) in filteredUserService"
              :key="`u` + index"
            >
              <ServiceCard :service="service" :remove="true" />
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-divider></v-divider>
      <v-card-text>
        {{ revokeText }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              depressed
              v-bind="attrs"
              v-on="on"
              color="error"
              class="ma-4"
            >
              <translate>Uninstall sciebo RDS</translate>
            </v-btn>
          </template>
          <v-card>
            <v-card-title class="headline">
              <translate>Uninstall sciebo RDS</translate>
            </v-card-title>

            <v-card-text>
              <translate tag="p">
                This will remove all services from RDS and all projects.
              </translate>
              <translate tag="p">This cannot be undone.</translate>
              <translate tag="p">Are you sure?</translate>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="error"
                text
                @click="
                  uninstallRDS();
                  dialog = false;
                "
              >
                <translate> Remove access to RDS </translate>
              </v-btn>
              <v-btn color="primary" @click="dialog = false">
                <translate> Cancel </translate>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
import ServiceCard from "./Card.vue";

export default {
  components: { ServiceCard },
  computed: {
    revokeText() {
      return this
        .$gettext(`If you want to remove all access in once or remove the access for your
          ownCloud account, click the "revoke button".`);
    },
    ...mapState({
      userservicelist: (state) => state.RDSStore.userservicelist,
      servicelist: (state) => state.RDSStore.servicelist,
    }),
    filteredServices() {
      return this.excludeServices(this.servicelist, this.userservicelist).sort(
        function (left, right) {
          return left.servicename.localeCompare(right.servicename);
        }
      );
    },
    filteredUserService() {
      return this.excludeServices(this.userservicelist, [
        {
          servicename: "port-owncloud",
        },
      ]).sort(function (left, right) {
        return left.servicename.localeCompare(right.servicename);
      });
    },
  },
  data: () => ({
    popup: undefined,
    overlay: false,
    zIndex: 1000,
    dialog: false,
  }),
  methods: {
    uninstallRDS() {
      this.$store.dispatch(
        "removeService",
        this.getInformations("port-owncloud")
      );
    },
  },
};
</script>
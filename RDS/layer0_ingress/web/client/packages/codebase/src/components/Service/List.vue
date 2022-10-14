<template>
  <v-container
    fluid
    class="pa-0 d-flex flex-column"
    style="margin-top: 13px;">
      <v-sheet
        flat
        height="6.3em"
        color="sidebar"
        style="border-bottom: 1px solid #ccc!important;"
        class="mb-4"
        max-width="100%" width="100%">

          <v-container fill-height>
              <v-row justify="space-around" class="overline">
                <v-col cols="auto">
                  Manage your repositories
                </v-col>
                <v-col cols="auto">
                  <!-- FIXME: this only works if owncloud / the PortIn is first in the userServiceList. Maybe use intersection of filteresServiceList and userServiceList -->
                  Currently Connected:  <span style="text-transform: none; font-size: 0.8rem"> {{userServiceList.slice(1).length > 0 ? userServiceList.slice(1).map((x) => x.displayName).join(", ") : 'None'}} </span>
                </v-col>
              </v-row>
          </v-container>

      </v-sheet>
  <v-row>
      <v-card flat v-for="(service, i) in filteredServiceList" :key="i" class="rounded-0 px-10" max-width="100%" width="100%" style="border-bottom: 1px solid #ccc;">
        <v-card-title>
        </v-card-title>
        <v-card-text>
          <ServiceConfiguration :service="service"  style="min-width: 100%"/>
        </v-card-text>
    </v-card>
  </v-row>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import ServiceConfiguration from "./Configuration.vue";

export default {
  components: {
    ServiceConfiguration,
  },
  computed: {
    ...mapState({
      userServiceList: (state) => state.RDSStore.userservicelist,
      serviceList: (state) => state.RDSStore.servicelist,
    }),
    filteredServiceList() {
      var filtered = [];
      for (var i of this.serviceList) {
        if (!i.servicename.startsWith("port-owncloud")) {
          filtered.push(i);
        }
      }
      return filtered;
    },
  },
  methods: {
    userUses(service) {
      for (var i of this.userServiceList) {
        if (i.servicename === service.servicename) {
          return true;
        }
      }
      return false;
    },
  },
};
</script>

<style lang="scss">
.v-expansion-panel-content__wrap {
  padding: 16px 24px 16px !important;
}

.v-expansion-panel-header--active {
  color: #3f50b5;
}
</style>

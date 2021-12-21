<template>
  <v-row justify="center">
    <v-expansion-panels inset focusable multiple>
      <v-expansion-panel v-for="(service, i) in filteredServiceList" :key="i">
        <v-expansion-panel-header>
          <v-row>
            <v-col cols="auto"> {{ service.displayName }}</v-col>
            <v-chip
              v-if="userUses(service)"
              color="light-green lighten-1"
              class="ma-2"
              small
              ><translate key="7d7908fe-afa8-4bf2-8435-cd8069672d1a">
                connected</translate
              >
              <v-icon class="ml-2">mdi-link</v-icon>
            </v-chip>
            <v-chip v-else color="grey" class="ma-2" small>
              <translate key="c4cd931f-852a-4d57-925a-31964bb6e862"
                >not connected</translate
              >
              <v-icon class="ml-2">mdi-link-off</v-icon>
            </v-chip>
          </v-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <ServiceConfiguration :service="service" />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-row>
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
      userservicelist: (state) => state.RDSStore.userservicelist,
      servicelist: (state) => state.RDSStore.servicelist,
    }),
    filteredServiceList() {
      var filtered = [];
      for (var i of this.servicelist) {
        if (i.servicename !== "port-owncloud") {
          filtered.push(i);
        }
      }
      return filtered;
    },
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

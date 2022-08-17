<template>
  <v-main style="padding: 0px">
    <v-layout column align-center wrap>
      <!-- hardcoded filter for owncloud, change -->
      <connect-service-warning v-if="!userHasServicesConnected" />
    </v-layout>
    <ServiceList />
  </v-main>
</template>

<script>
import { mapState } from "vuex";
import ServiceList from "../components/Service/List.vue";
import ConnectServiceWarning from "../components/common/ConnectServiceWarning.vue"

export default {
  components: {
    ServiceList,
    ConnectServiceWarning,
  },
  computed: {
    userHasServicesConnected() {
      let m = this.userservicelist.filter(s => s['implements'].includes('metadata'))
      if (m.length > 0) {
        return true;
      }
      return false;

    },
    ...mapState({
      userservicelist: (state) => state.RDSStore.userservicelist,
    }),
  },
};
</script>

<template>
  <v-main style="padding: 0px">
    <v-layout column align-center wrap>
      <!-- hardcoded filter for owncloud, change -->
      <v-alert
        dense
        type="error"
        class="mb-6"
        v-show="this.userservicelist.length < 2"
      >
        Please connect to at least one <strong>service</strong> to use RDS
      </v-alert>
    </v-layout>
    <ServiceList />
  </v-main>
</template>

<script>
import { mapState } from "vuex";
import ServiceList from "../components/Service/List.vue";

export default {
  components: {
    ServiceList,
  },
  computed: {
    ...mapState({
      userservicelist: (state) => state.RDSStore.userservicelist,
    }),
  },
};
</script>

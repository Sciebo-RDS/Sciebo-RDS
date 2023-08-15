<template>
  <v-container
    fluid
    class="pa-0 d-flex flex-column">
      <v-sheet
        flat
        height="6.3em"
        color="sidebar"
        style="border-bottom: 1px solid #ccc!important;"
        class="mb-4 px-10"
        max-width="100%" width="100%">

          <v-container fill-height>
            <!-- FIXME: make this row and columns behave like the columns below--> 
              <v-row  class="overline" align="center">
                <v-col xl="2" lg="3" md="3" sm="3" xs="12" class="text-center">
                  <span class="font-weight-bold">Manage your repositories</span>
                </v-col>
                  <v-col>
                    <v-card flat class="transparent mx-4">
                  Currently Connected:  <span style="text-transform: none; font-size: 0.8rem"> 
                    {{
                    filteredUserServiceList.length > 0
                    ?
                        ( filteredUserServiceList.length > 1
                      ?
                        [filteredUserServiceList.map((x) => x.displayName).slice(0, -1).join(', '),filteredUserServiceList.map((x) => x.displayName).slice(-1)].join(' and ')
                      :
                        filteredUserServiceList.map((x) => x.displayName).join(", "))
                    :
                      'None'}} </span>
                      </v-card>
                </v-col>
              </v-row>
          </v-container>

      </v-sheet>
  <v-row>
      <v-card flat v-for="(service, i) in filteredServiceList" :key="i" class="px-10" max-width="100%" width="100%" style="border-bottom: 1px solid #ccc;">
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
    //FIXME: make this independent from owncloud
    filteredServiceList() {
      return this.serviceList.filter(x => !x.servicename.startsWith("port-owncloud"));
    },
    //FIXME: make this independent from owncloud
    filteredUserServiceList() {
      return this.userServiceList.filter(x => !x.servicename.startsWith("port-owncloud"));
    }
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

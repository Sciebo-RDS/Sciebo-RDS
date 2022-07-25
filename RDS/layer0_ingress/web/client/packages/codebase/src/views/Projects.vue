<template>
  <v-main style="padding: 0px">
    <!-- move this into header bar-->
    <v-layout column align-end wrap v-if="userHasServicesConnected">
      <v-switch
        v-model="showAll"
        inset
        :label="$gettext('show past projects')"
      ></v-switch>
    </v-layout>

    <connect-service-warning v-else />

    <ProjectList />
    <!-- put these into their own components -->
    <v-card-text
      style="
        position: fixed;
        z-index: 1000;
        bottom: 70px;
        width: auto;
        right: 5px;
      "
    >
      <v-fab-transition>
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-show="true"
              color="error"
              dark
              absolute
              top
              right
              fab
              @click="collapseProjects"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-arrow-collapse</v-icon>
            </v-btn>
          </template>
          <span v-translate>Collapse all</span>
        </v-tooltip>
      </v-fab-transition>
    </v-card-text>
    <v-card-text
      style="
        position: fixed;
        z-index: 1000;
        bottom: 5px;
        width: auto;
        right: 5px;
      "
    >
      <v-fab-transition>
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-show="true"
              color="success"
              dark
              absolute
              top
              right
              fab
              @click="addProject"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-plus-thick</v-icon>
            </v-btn>
          </template>
          <span v-translate>New project</span>
        </v-tooltip>
      </v-fab-transition>
    </v-card-text>
  </v-main>
</template>

<script>
import { mapState } from "vuex";
import ProjectList from "../components/Project/List.vue";
import ConnectServiceWarning from "../components/common/ConnectServiceWarning.vue"

export default {
  components: {
    ProjectList,
    ConnectServiceWarning,
  },
  computed: {
    showAll: {
      get() {
        return this.$store.getters.showAllProjects;
      },
      set(val) {
        this.$store.commit("showAllProjects", val);
      },
    },
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
  methods: {
    collapseProjects() {
      this.$root.$emit("collapseProjects");
    },
    addProject() {
      this.$store.dispatch("createProject");
    },
  },
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>

<template>
  <v-row justify="center">
    <v-card
      v-if="projects.length == 0 && userHasServicesConnected"
      outlined
      tile
    >
      <v-card-title>
        <translate>No projects found</translate>
      </v-card-title>
      <v-card-text>
        <translate> Set the filter or create a new one project. </translate>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="addProject">
          <translate>Create a new project</translate>
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-expansion-panels inset focusable v-model="panel" v-else>
      <v-expansion-panel v-for="(project, i) in projects" :key="i">
        <v-expansion-panel-header>
          <v-row>
            <v-col class="d-inline-flex" style="max-width: fit-content !important;">
            <ProjectTitle v-bind:project="project" v-bind:active="panel === i" />
              </v-col>
            <v-col>
              <ProjectStatusChip
                v-bind:status="project.status"
                v-bind:class="{
                  'mt-2': panel === i && project.status < 4,
                  'mt-3': titleEdit && panel === i && project.status < 4,
                }"
                class="hidden-sm-and-down"
              />
              <ProjectStatusChip
                v-bind:status="project.status"
                class="hidden-md-and-up"
                v-bind:class="{
                  'mt-2': panel === i,
                  'hidden-md-and-down': titleEdit,
                }"
              />
            </v-col>
          </v-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <ProjectSetting
            @delete-project="deleteProject(project.researchIndex)"
            :project="project"
            v-if="panel === i"
          />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-row>
</template>

<style lang="scss">
.v-expansion-panel-content__wrap {
  padding: 16px 24px 16px !important;
}

.v-expansion-panel-header--active {
  color: #3f50b5;
}
</style>

<script>
import ProjectSetting from "./Setting.vue";
import ProjectStatusChip from "./StatusChip.vue";
import ProjectTitle from "./ProjectTitle.vue";
import { mapGetters } from "vuex";
import { mapState } from "vuex";

export default {
  components: {
    ProjectSetting,
    ProjectStatusChip,
    ProjectTitle,
  },
  data() {
    return {
      panel: [],
      projects: [],
    };
  },
  computed: {
    ...mapGetters({
      allProjects: "getProjectlist",
      showAllProjects: "showAllProjects",
    }),
    ...mapState({
      userservicelist: (state) => state.RDSStore.userservicelist,
    }),
    activeProjects() {
      return this.allProjects.filter((project) => project.status < 3);
    },
    userHasServicesConnected() {
      //hardcoded filter for owncloud, change
      if (this.userservicelist.length > 1) {
        return true;
      }
      return false;
    },
  },
  methods: {
    collapseProjects() {
      this.panel = [];
    },
    getProjects() {
      let projects = this.showAllProjects
        ? this.allProjects
        : this.activeProjects;

      return JSON.parse(JSON.stringify(projects)).sort((a, b) => {
        return b.status - a.status;
      });
    },
    deleteProject(researchIndex) {
      this.$store.dispatch("removeProject", { id: researchIndex });
      this.panel = [];
    },
    addProject() {
      this.$store.dispatch("createProject");
    },
  },
  created() {
    this.unwatch = this.$store.watch(
      (state, getters) => getters.showAllProjects,
      (newValue) => {
        this.projects = this.getProjects();

        this.panel = undefined;
      }
    );

    this.unwatch = this.$store.watch(
      (state, getters) => getters.getProjectlist,
      () => {
        this.projects = this.getProjects();
      }
    );
  },
  beforeMount() {
    this.projects = this.getProjects();
    console.log(
      "filter: ",
      this.showAllProjects,
      "active: ",
      this.activeProjects,
      "all: ",
      this.allProjects
    );
  },
  mounted() {
    this.$root.$on("collapseProjects", () => {
      this.collapseProjects();
    });
  },
  beforeDestroy() {
    this.$store.dispatch("requestProjectList");
    this.unwatch();
  },
};
</script>

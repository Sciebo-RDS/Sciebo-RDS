<template>
    <v-container
    fluid
    class="pa-0 d-flex flex-column"
    style="margin-top: 13px;">
    
<!-- <v-sheet flat height="8em"  color="error">

</v-sheet> -->

        <v-row no-gutters>

            <!-- Project list -->
            <v-col cols="3" class="col-xs-12">
                <!-- Project list header -->
                <v-sheet
                    flat
                    height="6.3em"
                    color="grey lighten-5"
                    style="border-bottom: 1px solid #ccc!important">
                    <v-container fill-height>
                        <v-row justify="center" class="overline">
                            {{ listtype == 'Current' ? activeProjects.length : pastProjects.length }} {{listtype}} Projects
                        </v-row>
                    </v-container>
                </v-sheet>

                <!-- Project list content -->
                <v-list max-height="calc( 100vh - 40px )" style="overflow-y: auto; margin: 0; padding: 0;">
                    <v-list-item-group>
                        
                        <div
                            @click="selectProject(p)"
                            active-class=""
                            v-for="p in (listtype == 'Current' ? activeProjects : pastProjects)"
                            :key="p.projectId"
                            class="grey lighten-5">
                        <v-list-item color="grey darken-3" style="border-bottom: 1px solid #ccc" >
                        <v-list-item-content
                            class="ma-1">
                            <v-row align="start">
                            <v-col class="caption">
                                Project
                                <v-list-item-title class="my-1" style="">
                                    <div class=" text-subtitle2 ">
                                {{ !!p.researchname ? p.researchname : 'Project ' + (p.researchIndex+1) }}
                                    </div>
                            </v-list-item-title>
                            </v-col>
                            <v-col class="d-flex flex-row-reverse">
                                <ProjectStatusChip
                                        v-bind:status="p.status"
                                    />
                            </v-col>
                            </v-row>
                            

                        </v-list-item-content>
                        
                        </v-list-item>
                        </div>
                    </v-list-item-group>
                </v-list>
                <!-- New Project button -->
                    <div v-if="listtype == 'Current'" class="text-center ma-6">
                    <v-btn
                        text
                        color="primary"
                        @click="addProject">
                            <v-icon class="ma-1">
                                mdi-plus
                            </v-icon>
                        new project
                    </v-btn>
                    </div>
            </v-col>

            <!-- Project Detail-->
            <v-col
                v-if="listtype == 'Current'"
                cols="9"
                style="border-left: 2px solid #ccc;">

                <!-- Active Project Stepper -->
                <v-card v-if="this.activeProject !== null" flat height="100%" >
                    <ProjectStepper :e1="e1" @setStepper="(n) => e1 = n" :project="allProjects.filter((i) => i.researchIndex == this.activeProject)[0]" style="min-height: 100%;"/>
                </v-card>

                <!-- No Project selected -->
                <v-card v-else flat height="100%">
                    <v-container fill-height >
                        <v-row align="center"
                            justify="center" class="overline">
                            <v-col cols="12" align="center">
                                <v-icon style="background-color: #eee; border-radius: 100%; padding: 5%;" size="35em">
                                    mdi-package-variant
                                </v-icon>
                            </v-col>
                            <br/>
                            Select a project or add a new one.
                        </v-row>
                    </v-container>
                </v-card>
            </v-col>

            <!-- Past Projects -->
            <v-col v-else cols="9" style="border-left: 2px solid #ccc;">
                <v-card v-if="this.activeProject !== null" flat height="100%" >
                    <!-- TODO: Past Project Detail View -->
                    <ArchiveProjectDetail :project="allProjects.filter((i) => i.researchIndex == this.activeProject)[0]" style="min-height: 100%;"/>
                </v-card>
                <v-card v-else flat height="100%">
                    <v-container fill-height >
                        <v-row v-if="pastProjects.length != 0" align="center"
                            justify="center" class="overline">
                            <v-col cols="12" align="center">
                                <v-icon style="background-color: #eee; border-radius: 100%; padding: 5%;" size="35em">
                                    mdi-package-variant
                                </v-icon>
                            </v-col>
                            <br/>
                                No project selected.
                        </v-row>
                        <v-row v-else align="center"
                            justify="center" class="overline">
                            <v-col cols="12" align="center">
                                <v-icon style="background-color: #eee; border-radius: 100%; padding: 5%;" size="35em">
                                    mdi-package-variant
                                </v-icon>
                            </v-col>
                            <br/>
                                You don't have any published or archived projects.
                        </v-row>
                    </v-container>
                </v-card>
            </v-col>
        </v-row>
    </v-container> 
</template>


<script>
import ProjectStatusChip from "./StatusChip.vue";
import ProjectStepper from "./Stepper.vue";
import ArchiveProjectDetail from "../Archive/ProjectDetail.vue";
import { mapGetters } from "vuex";
import { mapState } from "vuex";

export default {
  components: {
    ProjectStatusChip,
    ProjectStepper,
    ArchiveProjectDetail,
  },
  data() {
    return {
      projects: [],
      e1: 1,
    };
  },
  props: ["listtype",],
  computed: {
    ...mapGetters({
      allProjects: "getProjectlist",
      showAllProjects: "showAllProjects",
    }),
    ...mapState({
      userservicelist: (state) => state.RDSStore.userservicelist,
    }),
    activeProject: {
        get() {
            return this.$store.getters.getActiveProject
        },
        set(value) {
            this.$store.commit('setActiveProject', value)
        }
    },
    activeProjects() {
      return this.allProjects.filter((project) => project.status < 3);
    },
    pastProjects(){
      return this.allProjects.filter((project) => project.status >= 3);
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
    getProjects() {
      let projects = this.showAllProjects
        ? this.allProjects
        : this.activeProjects;

      return JSON.parse(JSON.stringify(projects)).sort((a, b) => {
        return b.status - a.status;
      });
    },
    selectProject(p){
      console.log(this.activeProject)
      this.e1 = 1
      this.activeProject = p.researchIndex;
    },
    deleteProject(researchIndex) {
      this.$store.dispatch("removeProject", { id: researchIndex });
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
    this.activeProject = null;
  },
};
</script>

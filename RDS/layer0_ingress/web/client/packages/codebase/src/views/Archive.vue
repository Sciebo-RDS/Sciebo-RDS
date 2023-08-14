<template>
    <v-main
      class="pa-0 ma-0">
      
      <v-sheet
        flat
        height="6.3em"
        color="grey lighten-5"
        style="border-bottom: 1px solid #ccc!important">
        <v-container fill-height>
            <v-row class="overline" align="center">
              <span class="font-weight-bold">Published Projects</span>
            </v-row>
        </v-container>
      </v-sheet>

      <v-container class="ma-3">
        <div v-for="project in publishedProjects" :key="project.researchIndex">
          <ProjectCard :project="project" />
        </div>
      </v-container>
    
  </v-main>
</template>

<script>
import ProjectCard from "../components/Archive/ProjectCard.vue";
import { mapGetters } from "vuex";

export default {
  components: {
    ProjectCard,
  },
  computed: {
    ...mapGetters({
      projects: "getProjectlist",
    }),
    publishedProjects(){
      return this.projects.filter((project) => project.status == 3);
    },
  },
  methods: {
  },
};
</script>

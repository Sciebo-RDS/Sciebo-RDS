<template>
    <v-main
      class="pa-0 ma-0" >
      
      <v-sheet
        flat
        height="6.3em"
        color="sidebar"
        style="border-bottom: 1px solid #ccc!important;">
        <v-container fill-height>
            <v-row class="overline text-center" justify="center" align="center">
              {{ publishedProjects.length > 0 ? publishedProjects.length : 'No' }} Published {{ publishedProjects.length === 1 ? "Project" : "Projects" }}
            </v-row>
        </v-container>
      </v-sheet>

      <v-container v-if="publishedProjects.length > 0" class="d-flex ma-1">
          <ProjectCard v-for="project in publishedProjects" :key="project.researchIndex" :project="project" />
      </v-container>

      <v-container v-else fill-height >
        <v-row align="center"
          justify="center" class="overline">
          <v-col cols="12" align="center">
            <v-icon style="color: #d6e2e2; border-radius: 100%; padding: 5%;" size="35em">
                  mdi-package-variant
            </v-icon>
          </v-col>
              <br/>
                  You haven't published any projects yet.
        </v-row>
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
      return this.projects.filter((project) => project.status == 3).reverse();
    },
  },
  methods: {
  },
};
</script>

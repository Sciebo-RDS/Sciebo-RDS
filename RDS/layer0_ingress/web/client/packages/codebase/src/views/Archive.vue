<template>
    <v-main
      class="pa-0 ma-0" >
      
      <v-sheet
        flat
        height="6.3em"
        color="grey lighten-5"
        style="border-bottom: 1px solid #ccc!important;">
        <v-container fill-height>
            <v-row class="overline text-center" justify="center" align="center">
              Published Projects
            </v-row>
        </v-container>
      </v-sheet>

      <v-container v-if="publishedProjects.length > 0" class="d-flex ma-1">
          <ProjectCard v-for="project in publishedProjects" :key="project.researchIndex" :project="project" />
      </v-container>

      <v-container v-else fill-height >
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
      return this.projects.filter((project) => project.status == 3);
    },
  },
  methods: {
  },
};
</script>

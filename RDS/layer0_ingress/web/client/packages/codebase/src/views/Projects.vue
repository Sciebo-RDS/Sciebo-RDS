<template>
    <v-main
      class="pa-0 ma-0">
    <ProjectList style="height: 100vh;" listtype="Current">
      Current
    </ProjectList>
  </v-main>
</template>

<script>
import ProjectList from "../components/Project/List.vue";

export default {
  components: {
    ProjectList,
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
  },
  methods: {
  },
  beforeDestroy() {
    this.$store.commit('resetLoadedProject')
  }  
};
</script>

<template>
    <v-main
      class="pa-0 ma-0">
    <ProjectList style="height: calc( 100vh - 25px );" listtype="Past">
      Published
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
  },
  methods: {
  },
  beforeDestroy() {
    this.$store.commit('resetLoadedProject')
  }
};
</script>

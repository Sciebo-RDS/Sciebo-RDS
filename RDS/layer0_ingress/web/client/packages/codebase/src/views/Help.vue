<template>

  <div class="px-10 py-8 ma-5 grey lighten-5">
    <RenderHelp
      v-for="(questions, category) in help_categories[this.$config.language]"
      :key="category"
      :category="category"
      :questions="questions"/>
  </div>

</template>

<script>
import { mapGetters } from "vuex";
import RenderHelp from '../components/Help/RenderHelp.vue'

export default {
  name: "Help",
  components: {
    RenderHelp,
  },
  computed: {
    ...mapGetters({ help_categories: "getQuestions" }),
  },
};
</script>

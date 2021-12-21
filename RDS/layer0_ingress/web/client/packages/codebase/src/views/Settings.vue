<template>
  <v-container flex>
    <v-row>
      <v-col v-if="!languagePredefined"><LanguageSelector /></v-col>
      <v-col><ThemeSelector /></v-col>
    </v-row>
    <v-row>
      <v-col><ServiceEditor /></v-col>
    </v-row>
  </v-container>
</template>

<script>
import LanguageSelector from "../components/Settings/LanguageSelector.vue";
import ThemeSelector from "../components/Settings/ThemeSelector.vue";
import ServiceEditor from "../components/Service/Editor.vue";

export default {
  components: {
    LanguageSelector,
    ThemeSelector,
    ServiceEditor,
  },
  computed: {
    languagePredefined() {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.has("lang");
    },
  },
};
</script>

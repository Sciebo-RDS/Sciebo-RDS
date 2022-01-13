<template>
  <v-card class="mx-auto pa-4" min-width="250px">
    <v-card-title v-translate>Settings for language</v-card-title>
    <v-select
      :items="availableLanguages"
      item-value="short"
      item-text="long"
      :label="$gettext('Select language')"
      v-model="language"
    ></v-select>
  </v-card>
</template>

<script>
export default {
  name: "LanguageSelector",
  computed: {
    language: {
      set(value) {
        this.$config.language = value;
        this.$store.dispatch("setLanguage", { language: value });
      },
      get() {
        return {
          short: this.$store.getters.getLanguage,
          long: this.$language.available[this.$store.getters.getLanguage],
        };
      },
    },
    availableLanguages: function () {
      let res = [];
      for (const [key, value] of Object.entries(this.$language.available)) {
        res.push({ short: key, long: value });
      }

      return res;
    },
  },
};
</script>
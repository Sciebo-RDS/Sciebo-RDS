<template>
  <v-row justify="center" class="pt-10">
    <v-progress-circular
      indeterminate
      color="primary"
      size="64"
      v-if="Object.keys(help_categories).length === 0"
    >
      <translate>Wait</translate>
    </v-progress-circular>
    <v-expansion-panels
      inset
      focusable
      multiple
      v-else
      v-for="(questions, category) in help_categories[this.$config.language]"
      :key="category"
      style="padding-top: 30px"
    >
      <div class="text-h6" v-text="category" />
      <v-expansion-panel v-for="(answer, question) in questions" :key="answer">
        <v-expansion-panel-header>
          {{ question }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <span v-html="markdown(answer)" />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-row>
</template>

<script>
import marked from "marked";
import DOMPurify from "dompurify";
import { mapGetters } from "vuex";

const renderer = new marked.Renderer();
const linkRenderer = renderer.link;
renderer.link = (href, title, text) => {
  const localLink = href.startsWith(
    `${location.protocol}//${location.hostname}`
  );
  const html = linkRenderer.call(renderer, href, title, text);
  return localLink
    ? html
    : html.replace(
        /^<a /,
        `<a target="_blank" rel="noreferrer noopener nofollow" `
      );
};

export default {
  name: "Help",
  computed: {
    ...mapGetters({ help_categories: "getQuestions" }),
  },
  data() {
    return {
      panel: [],
    };
  },
  methods: {
    markdown(text) {
      const html = marked(text, { renderer });

      return DOMPurify.sanitize(html, { ADD_ATTR: ["target"] });
    },
  },
};
</script>

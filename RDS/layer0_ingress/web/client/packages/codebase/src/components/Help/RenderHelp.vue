<template>
    <div>
        <v-divider/>
            <div class="pa-2 text-center text-h5 ma-3">
                {{category}}
            </div>
        <div v-for="(answer, question) in questions" :key="question" class="my-3">
            <v-divider class="mb-5"/>
            <v-row>
                <v-col class="text-subtitle-1 col-xl-3 col-lg-4 col-md-5 col-12" style="word-break: break-word">
                    {{question}}
                </v-col>
                <v-col class="text-subtitle-2" style="word-break: break-word">
                    <span v-html="markdown(answer)" />
                </v-col>
            </v-row>
        </div>
    </div>
</template>

<script>
import marked from "marked";
import DOMPurify from "dompurify";

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
    props: ["category", "questions"] ,
    methods: {
        markdown(text) {
            const html = marked(text, { renderer });

            return DOMPurify.sanitize(html, { ADD_ATTR: ["target"] });
        },
    },
};
</script>

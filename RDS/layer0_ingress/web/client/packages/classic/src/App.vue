<template>
  <div
    class="uk-flex uk-flex-center uk-flex-middle uk-height-1-1 uk-width-1-1"
    style="width: 100%; height: 100%"
  >
    <oc-spinner
      v-if="loading"
      aria-label="Loading..."
      class="uk-position-center"
      size="xlarge"
      style="width: 100%; height: 100%"
    />
    <iframe
      class="uk-height-1-1 uk-width-1-1"
      v-else
      id="rds-editor"
      ref="rdsEditor"
      :src="iframeSource"
      crossorigin="use-credentials"
      style="width: 100%; height: 100%"
    />
  </div>
</template>

<script>
import queryString from "querystring";
import getConfig from "./plugins/values.js";

export default {
  data: () => ({
    loading: true,
    config: {},
  }),
  computed: {
    iframeSource() {
      const query = queryString.stringify({
        embed: 1,
        lang: this.config.language.split("_")[0],
      });
      return `${this.config.url}?${query}`;
    },
    rdsWindow() {
      return this.$refs.rdsEditor.contentWindow;
    },
    headers() {
      return new Headers({
        requesttoken: oc_requesttoken,
        "Content-Type": "application/json",
      });
    },
  },
  methods: {
    error(error) {
      console.log(error);
    },
    sendLocationToWindow(projectId, location) {
      this.rdsWindow.postMessage(
        JSON.stringify({
          event: "filePathSelected",
          data: {
            projectId: projectId,
            filePath: location,
          },
        }),
        "*"
      );
    },
    sendInformationsToWindow() {
      this.rdsWindow.postMessage(
        JSON.stringify({
          event: "informations",
          data: this.config.response,
        }),
        "*"
      );
    },
  },
  created() {
    getConfig(this).then(() => {
      this.loading = false;
    });

    window.addEventListener("message", (event) => {
      if (event.data.length > 0) {
        var payload = JSON.parse(event.data);
        switch (payload.event) {
          case "init":
            this.sendInformationsToWindow();
            break;
          case "showFilePicker":
            let location = "";
            OC.dialogs.filepicker(
              t("files", "Choose source folder"),
              (targetPath, type) => {
                location = targetPath.trim();
                this.sendLocationToWindow(payload.data.projectId, location);
              },
              false,
              "httpd/unix-directory",
              true
            );
            break;
          case "filePathSelected":
            let data = payload.data;
            this.currentFilePath = data.filePath;
            this.$store.commit("setModifiedFilePath", this.currentFilePath);
            break;
        }
      }
    });
  },
};
</script>

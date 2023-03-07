<template>
  <div class="text-center">
    <v-container flex v-if="loading">
      <v-row>
        <v-col>
          <v-progress-circular indeterminate color="primary" />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          {{ loadingText }}
        </v-col>
      </v-row>
    </v-container>
    <div style="height: calc(100vh - 13em);">
    <iframe
      v-if="dataAvailable"
      v-show="!loading"
      id="describoWindow"
      ref="describoWindow"
      :src="iframeSource"
      width="100%"
      style="border: 0px; left: 0px; height: 100%"
      @load="loaded()"
    ></iframe>
    </div>
  </div>
</template>

<script>
import queryString from "querystring";
import { mapGetters } from "vuex";

export default {
  props: ["project"],
  data: () => ({
    dataAvailable: false,
    loading: true,
    loadingText: "",
    sessionId: undefined,
  }),
  computed: {
    ...mapGetters({
      ownCloudServicename: "getOwnCloudServername",
      loadedFilePath: "getLoadedFilePath",
      loadedPortOut: "getLoadedPortOut",
      metadataProfile: "getLoadedMetadataProfile"
    }),
    editor() {
      return this.$refs.describoWindow.contentWindow;
    },
    parent() {
      return window.parent;
    },
    iframeSource() {
      const query = queryString.stringify({
        embed: 1,
        sid: this.sessionId,
      });
      return `${this.$config.describo}?${query}`;
    },
  },
  watch: {
    loadedFilePath(newLoadedFilePath, oldLoadedFilePath){
      if (!!newLoadedFilePath){
        this.initDescribo(this.loadedFilePath, this.metadataProfile);
      }
    },
    loadedPortOut(newLoadedPortOut, oldLoadedPortOut) {
      this.initDescribo(this.loadedFilePath, this.metadataProfile);
    },
    metadataProfile(newMetadataProfile, oldMetadataProfile) {
      this.initDescribo(this.loadedFilePath, this.metadataProfile);
    },
  },
  methods: {
    loaded() {
      this.loading = false;
    },
    eventloop(event) {
      if (event.data.length > 0) {
        var payload = JSON.parse(event.data);
        switch (payload.event) {
          case "init":
          case "load":
            this.parent.postMessage(
              JSON.stringify({
                event: "load",
                data: {
                  projectId: this.project.projectId,
                  filePath: this.loadedFilePath,
                },
              }),
              "*"
            );
            break;
          case "save":
          case "autosave":
            this.parent.postMessage(
              JSON.stringify({
                event: "save",
                data: {
                  projectId: this.project.projectId,
                  filePath: this.loadedFilePath,
                  fileData: this.fileData,
                },
              }),
              "*"
            );
            break;
          case "loaded":
            this.editor.postMessage(
              JSON.stringify({
                event: "loaded",
                data: payload.data,
              })
            );
            break;
          case "filesList":
            this.editor.postMessage(
              JSON.stringify({
                event: "filesList",
                data: payload.data,
              })
            );
        }
      }
    },
    initDescribo(filePath, metadataProfile) {
      if (filePath == null || filePath === "") {
        return;
      }

      this.$socket.client.emit(
        "requestSessionId",
        { folder: filePath, metadataProfile },
        (sessionId) => {
          this.dataAvailable = true;
          this.sessionId = sessionId;
        }
      );

      this.standardLoadingText = this.$gettext("Editor loading");
      this.loadingText = this.standardLoadingText;
      let counter = 0;
      let loader = setInterval(() => {
        if (!this.loading) {
          this.loadingText = "Done loading";
          clearInterval(loader);
        }

        if (counter > 30) {
          this.loadingText = this.$gettext(
              "Error while loading. Please contact an administator."
          );
          clearInterval(loader);
        } else {
          if (counter % 4 > 0) {
            this.loadingText += ".";
          } else {
            this.loadingText = this.standardLoadingText;
          }
          counter += 1;
        }
      }, 1000);
    }
  },
  beforeMount() {
    this.dataAvailable = false;

    this.$root.$on("projectReloaded", (args) => {
      this.initDescribo(args.filePath, args.metadataProfile);
    });
  },
  created() {
    window.addEventListener("message", this.eventloop);
  },
  beforeDestroy() {
    window.removeEventListener("message", this.eventloop);
  },
};
</script>

<style></style>

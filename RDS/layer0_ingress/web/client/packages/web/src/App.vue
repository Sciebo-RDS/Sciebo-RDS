<template>
  <div class="uk-flex uk-flex-center uk-flex-middle uk-height-1-1 uk-width-1-1">
    <oc-spinner
      v-if="loading"
      :aria-label="$gettext('Loading media')"
      class="uk-position-center"
      size="xlarge"
    />
    <iframe
      class="uk-height-1-1 uk-width-1-1"
      v-else
      v-show="!showFilePicker"
      id="rds-editor"
      ref="rdsEditor"
      :src="iframeSource"
      :disabled="showFilePicker"
    />
    <oc-modal
      v-if="showFilePicker"
      icon="search"
      title="Select a folder"
      :buttonConfirmDisabled="true"
      class="uk-position-relative"
      :focus-trap-active="showFilePicker"
      @cancel="hideFilePicker"
    >
      <template v-slot:content>
        <file-picker
          ref="file-picker"
          variation="location"
          :bearerToken="getToken"
          :is-sdk-provided="true"
          :config-object="{}"
          @selectResources="handleFilePick"
        />
      </template>
    </oc-modal>
  </div>
</template>

<script>
import queryString from "querystring";
import { mapGetters, mapActions } from "vuex";
import FilePicker from "@ownclouders/file-picker";

export default {
  components: {
    FilePicker,
  },
  data: () => ({
    loading: true,
    showFilePicker: false,
    latestPayloadFromFrame: {},
    active: true,
  }),
  computed: {
    ...mapGetters(["getToken"]),
    config() {
      const {
        url = "http://localhost:8085",
        server = this.$store.state.config.server,
        autosave = false,
        describo = "http://localhost:8100",
      } =
        this.$store.state.apps.fileEditors.find(
          (editor) => editor.app === "rds"
        ).config || {};
      return { url, server, autosave, describo };
    },
    iframeSource() {
      const query = queryString.stringify({
        embed: 1,
      });
      return `${this.config.url}?${query}`;
    },
    rdsWindow() {
      return this.$refs.rdsEditor.contentWindow;
    },
    headers() {
      return new Headers({
        Authorization: "Bearer " + this.getToken,
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
      });
    },
  },
  methods: {
    ...mapActions(["showMessage"]),
    error(error) {
      console.log(response);
      this.showMessage({
        title: this.$gettext("The rds could not be loaded…"),
        desc: error,
        status: "danger",
        autoClose: {
          enabled: true,
        },
      });
    },
    load(filePath) {
      this.$client.files
        .getFileContents(filePath, { resolveWithResponseObject: true })
        .then((resp) => {
          this.rdsWindow.postMessage(
            JSON.stringify({
              action: "load",
              xml: resp.body,
              autosave: this.config.autosave,
            }),
            "*"
          );
        })
        .catch((error) => {
          this.error(error);
        });
    },
    save(filePath, payload) {
      this.$client.files
        .putFileContents(filePath, payload.xml, {
          previousEntityTag: this.currentETag,
        })
        .then((resp) => {
          this.currentETag = resp.ETag;
          this.rdsWindow.postMessage(
            JSON.stringify({
              action: "status",
              modified: false,
            }),
            "*"
          );
        })
        .catch((error) => {
          this.error(error);
        });
    },
    exit() {
      window.close();
    },
    hideFilePicker() {
      this.showFilePicker = false;
    },
    handleFilePick(event) {
      this.hideFilePicker();
      const location = event[0].path;
      this.rdsWindow.postMessage(
        JSON.stringify({
          event: "filePathSelected",
          data: {
            projectId: this.latestPayloadFromFrame.projectId,
            filePath: location,
          },
        }),
        "*"
      );
    },
    eventloop(event) {
      if (event.data.length > 0) {
        let payload = JSON.parse(event.data);
        let data = payload.data;
        this.latestPayloadFromFrame = data;

        switch (payload.event) {
          case "init":
            let url = `${this.config.server}/index.php/apps/rds/api/1.0/informations`;
            fetch(url, { headers: this.headers })
              .then((response) => {
                if (response.ok) {
                  return response.text();
                }

                throw new Error(`${response.status} ${response.statusText}`);
              })
              .then((resp) => {
                this.rdsWindow.postMessage(
                  JSON.stringify({
                    event: "informations",
                    data: resp,
                  }),
                  "*"
                );
              })
              .catch((error) => {
                this.loading = true;
                this.error(error);
              });
            break;
          case "showFilePicker":
            this.showFilePicker = true;
            break;
          case "load":
            this.rdsWindow.postMessage(
              JSON.stringify({
                event: "loaded",
                data: {
                  projectId: data.projectId,
                  filePath: data.filePath,
                  fileData: this.load(data.filePath),
                },
              }),
              "*"
            );
            break;
          case "save":
            this.save(data.filePath, data.fileData);
            break;
          case "exit":
            this.exit();
            break;
        }
      }
    },
  },
  mounted() {
    this.loading = false;
    window.addEventListener("message", this.eventloop);
  },
  beforeDestroy() {
    window.removeEventListener("message", this.eventloop);
  },
};
</script>

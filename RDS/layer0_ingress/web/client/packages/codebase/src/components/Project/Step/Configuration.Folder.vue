<template>
  <v-card flat class="mb-2 d-flex flex-column">
    <v-list two line>
      <v-list-item>
        <v-list-item-avatar size="3em" class="align-self-start">
          <v-icon
            size="2em"
            color="black"
            class="grey lighten-2 rounded-circle pa-16 mx-auto my-8"
          >
            mdi-numeric-1
          </v-icon>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title
            class="text-h6 self-align-start text-wrap"
            style="line-height: 2em"
          >
            <v-row justify="space-around">
              <v-col cols="auto" class="mr-auto">
                Select your project folder.
              </v-col>
              <v-col cols="auto" class="text-right">
                <v-icon color="error" v-if="!hasFolder">
                  mdi-alert-circle-outline
                </v-icon>
                <v-icon color="success" class="outlined" v-else>
                  mdi-check-circle-outline
                </v-icon>
              </v-col>
            </v-row>
          </v-list-item-title>
          <v-list-item-subtitle v-if="!hasFolder" class="py-1 text-wrap">
            <v-btn outlined color="warning" class="mr-1" @click="togglePicker">
              Pick
            </v-btn>
            a folder to add metadata to and publish. This folder will be loaded
            from your sciebo account.
          </v-list-item-subtitle>
          <v-list-item-subtitle v-else class="py-1 text-wrap">
            <v-btn
              text
              outlined
              color="primary"
              class="mr-1"
              @click="togglePicker"
            >
              Pick
            </v-btn>
            a folder to add metadata to and publish. This folder will be loaded
            from your sciebo account.
          </v-list-item-subtitle>

          <v-row v-if="hasFolder" align="center" class="mt-2">
            <v-col
              md="auto"
              class="grey--text text--darken-3 text-caption text-decoration-underline"
            >
              Currently selected:
            </v-col>
            <v-col md="auto" class="grey--text text--darken-2">
              {{ loadedFilePath }}
            </v-col>
          </v-row>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data: () => ({}),
  beforeMount() {
    window.addEventListener("message", this.eventloop);
  },
  beforeDestroy() {
    window.removeEventListener("message", this.eventloop);
  },
  computed: {
    ...mapGetters({
      loadedResearchId: "getLoadedResearchId"
    }),
    loadedFilePath: {
      get() {
        return this.$store.getters.getLoadedFilePath;
      },
      set(value) {
        this.$store.commit("setLoadedFilePath", value);
      },
    },
    hasFolder() {
      return !!this.loadedFilePath
    },
  },
  methods: {
    eventloop(event) {
      if (event.data.length > 0) {
        var payload = JSON.parse(event.data);
        console.log("event received in Folder.vue");
        switch (payload.event) {
          case "filePathSelected":
            let data = payload.data;
            console.log("filepathselected received in Folder.vue");
            console.log("data: " + this.data + " Folder.vue");
            if (data.projectId == this.loadedResearchId) {
              this.loadedFilePath = data.filePath;
            }
            break;
        }
      }
    },
    togglePicker() {
      this.showFilePicker(this.loadedResearchId, (!!this.loadedFilePath ? this.loadedFilePath : "/"));
    },
  },
};
</script>

<template>
  <div style="height: 100%">
    <v-stepper v-model="e1" alt-labels flat style="height: 100%">
      <!-- Stepper header -->
      <v-stepper-header
      style="
      box-shadow: none !important;
      padding-bottom: 1px;
      border-bottom: 1px solid #ccc;"
      :style="$vuetify.theme.dark === true ? 'background-color: #1e1e1e': 'background-color: #f5f5f5'">
        <v-stepper-step :complete="e1 > 1" step="1">
          <translate>Configuration</translate>
        </v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step :complete="e1 > 2" step="2">
          <translate>Metadata</translate>
        </v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step step="3">
          <translate>Publish</translate>
        </v-stepper-step>
      </v-stepper-header>

      <!-- Step 1: Configuration -->
      <v-stepper-items style="height: 100%">
        <v-stepper-content step="1" class="pa-0">
          <v-card
            flat
            class="overflow-y-auto"
            style="height: calc(100vh - 12.9em)"
          >
            <StepConfiguration
              :project="project"
            />
          </v-card>
        </v-stepper-content>

        <!-- Step 2: Metadata -->
        <v-stepper-content step="2" class="pa-0">
          <v-card
            class="d-flex flex-column justify-center"
            min-height="500px"
            flat
            style="height: calc(100vh - 12.9em);"
          >
            <StepMetadataEditor :project="project" />
          </v-card>
        </v-stepper-content>

        <!-- Step 3: Publish -->
        <v-stepper-content step="3" class="pa-0">
          <v-card
            flat
            class="pa-3 overflow-y-auto"
            style="height: calc(100vh - 12.9em);">
            <StepPublish :published="published" :publishInProgress="publishInProgress" :project="project"/>
          </v-card>
        </v-stepper-content>
      </v-stepper-items>

      <!-- Stepper navigation buttons -->

      <v-sheet
        flat
        height="5em"
        color="sidebar"
        style="bottom: 0%; position: absolute; right: 0%; border-top: 1px solid #ccc!important"
        width="100%"
      >
        <!-- config nav -->
        <v-flex v-if="e1 == 1" class="d-flex mb-6">


          <!-- Delete Project Dialog & Button -->

            <v-dialog
              v-if="!publishInProgress && !published"
              v-model="deleteDialog"
              persistent
              width="auto"
              max-width="60%"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  outlined
                  class="mr-auto ma-5"
                  color="error"
                  dark
                  v-bind="attrs"
                  v-on="on"
                >
                  Delete
                </v-btn>
             </template>
              <v-card class="pa-5">
                <v-card-title class="text-h5">
                  Please confirm
                </v-card-title>
                <v-card-text class="pb-5 pt-3">Are you sure you want to delete {{ loadedResearchName !== "" ? `<span class="font-weight-bold">${loadedResearchName}</span>` : "this project" }}?</v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>?
                  <v-btn
                    color="error"
                    depressed
                    @click="archiveProject(loadedProject.researchIndex)"
                    class="pa-4"
                  >
                    Delete
                  </v-btn>
                  <v-btn
                    color="primary"
                    text
                    @click="deleteDialog = false"
                    class="pa-4"
                  >
                    Cancel
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          <v-flex class="text-right">

          <!-- Delete Dialog End-->

            <v-btn
            :disabled="!isConfigComplete"
            color="primary"
            @click="[sendChanges(), ($emit('setStepper', 2))]"
            class="ma-5"
          >
              Continue
            </v-btn>
          </v-flex>
        </v-flex>


        <!-- metadata nav -->

            <v-flex v-if="e1 == 2" class="text-right">
                <v-btn outlined @click="$emit('setStepper', 1)">
                <!-- <translate>Back</translate> -->
                    Back
                </v-btn>

                <v-btn color="primary" @click="$emit('setStepper', 3)" class="ma-5">
                <!-- <translate>Continue</translate> -->
                    Continue
                </v-btn>
            </v-flex>

        <!-- publish nav -->

          <v-flex v-if="e1 == 3" class="text-right">
            <v-btn outlined @click="$emit('setStepper', 2)" class="">
              <!--  <translate>Back</translate> -->
              Back
            </v-btn>

            <v-btn
              :disabled="publishInProgress || published"
              color="success"
              @click="publishProject"
              class="ma-5"
            >
              <translate v-if="publishInProgress">In progress...</translate>
              Publish
            </v-btn>
          </v-flex>
      </v-sheet>

      <!-- / Stepper buttons-->
    </v-stepper>
  </div>
</template>


<script>
import { mapGetters } from "vuex";
import StepConfiguration from "./Step/Configuration.vue";
import StepPublish from "./Step/Publish.vue";
import StepMetadataEditor from "./Step/MetadataEditor.vue";

export default {
  components: {
    StepConfiguration,
    StepPublish,
    StepMetadataEditor,
  },
  data() {
    return {
      publishInProgress: false,
      published: false,
      deleteDialog: false,
    };
  },
  computed: {
    ...mapGetters({
      loadedResearchName: "getLoadedResearchName",
      loadedProject: "getLoadedProject",
      loadedFilePath: "getLoadedFilePath",
      loadedResearchIndex: "getLoadedResearchIndex",
      loadedMetadataProfile: "getLoadedMetadataProfile",
      originalResearchName: "getOriginalResearchNameForLoadedProject",
      originalFilePath: "getOriginalFilePathForLoadedProject",
      originalPortInForLoadedProject: "getOriginalPortInForLoadedProject",
      originalPortOutForLoadedProject: "getOriginalPortOutForLoadedProject",
      ownCloudServername: "getOwnCloudServername",
    }),
    isConfigComplete() {
      return this.hasFolder && this.hasService && this.hasResearchName;
    },
    hasFolder() {
      return !!this.loadedFilePath;
    },
    hasService() {
      return this.loadedProject.portOut.length > 0;
    },
    hasResearchName() {
       return !!this.loadedResearchName || !!this.originalResearchName;
    },
    portChanges() {
      let changes = this.computePortChanges()
      return changes
    }
  },
  watch: {
    loadedResearchIndex(newLoadedResearchIndex, oldLoadedResearchIndex) {
        if (newLoadedResearchIndex !== oldLoadedResearchIndex) {
            this.published = (this.loadedProject.status == '3');
        }
    }
  },
  props: ["project", "e1"],
  methods: {
    computePortChanges() {
      let loadedPortOutNames = this.loadedProject["portOut"].map((s) => s.port)
      let originalPortOutNames = this.originalPortOutForLoadedProject.map((s) => s.port)
      return {
        researchIndex: this.loadedProject["researchIndex"],
        import: {
          add:
                (this.loadedProject["portIn"].length == 0) ?
                  [{
                    "servicename": "port-owncloud-" + this.ownCloudServername,
                    "filepath": this.loadedFilePath,
                  }]
                : []
              ,
          remove: [],
          change:
                (this.loadedProject["portIn"].length > 0 && this.loadedFilePath !== this.originalFilePath)
          ?
                  [{
                    "servicename": "port-owncloud-" + this.ownCloudServername,
                    "filepath": this.loadedFilePath,
                  }]
                : [],
        },
        export: {
          add: loadedPortOutNames.filter(p => !originalPortOutNames.includes(p)).map(function (x) { return {"servicename": x} }),
          remove: originalPortOutNames.filter(p => !loadedPortOutNames.includes(p)).map(function (x) { return {"servicename": x} }),
          change: []
        }
      }
    },
    async sendChanges() {
      if (!!this.loadedResearchName && this.originalResearchName !== this.loadedResearchName) {
        this.$store.dispatch("changeResearchname", {
          researchIndex: this.loadedProject["researchIndex"],
          researchname: this.loadedResearchName,
        });
      }
      await this.$store.dispatch("changePorts", this.portChanges);
      this.emitProjectReloaded();
    },
    emitProjectReloaded() {
      this.$root.$emit("projectReloaded", {filePath: this.loadedFilePath, metadataProfile: this.loadedMetadataProfile});
    },
    archiveProject(rId) {
      this.$store.commit('setLoadedProject', null)
      this.$store.dispatch("removeProject", { id: rId });
    },
    publishProject() {
      this.publishInProgress = true;

      this.$root.$emit(
        "showsnackbar",
        this.$gettext(
          "The publishing process will start now. We will inform you when it finishes."
        )
      );

      this.$socket.client.emit(
        "triggerSynchronization",
        {
          researchIndex: this.project["researchIndex"],
        },
        (result) => {
          let text = this.$gettext(
            "There was an error publishing your project. Please check if you filled all fields in the metadata step."
          );
          if (result) {
            text = this.$gettext("Your project '" + this.project["researchname"] + "' was successfully published.");
            this.published = true;
          }

          this.$root.$emit("showsnackbar", text);
          this.publishInProgress = false;
        }
      );
    },
  },
};
</script>

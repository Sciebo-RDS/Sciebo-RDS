<template>
  <div style="height: 100%">
    <v-stepper v-model="e1" alt-labels flat style="height: 100%">
      <!-- Stepper header -->
      <v-stepper-header style="box-shadow: none !important">
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
            height="auto"
            flat
            class="overflow-y-auto"
            style="max-height: calc(100vh - 12.9em)"
          >
            <StepConfiguration
              :project="project"
              @changePorts="receiveChanges"
            />
          </v-card>
        </v-stepper-content>

        <!-- Step 2: Metadata -->
        <v-stepper-content step="2">
          <v-card
            class="d-flex flex-column justify-center mb-12"
            min-height="500px"
            flat
          >
            <StepMetadataEditor :project="project" />
          </v-card>
        </v-stepper-content>

        <!-- Step 3: Publish -->
        <v-stepper-content step="3">
          <v-card class="mb-12" height="auto" flat>
            <StepPublish :project="project" />
          </v-card>
        </v-stepper-content>
      </v-stepper-items>

      <!-- Stepper navigation buttons -->

      <v-sheet
        flat
        height="5em"
        color="grey lighten-5"
        style="bottom: 0%; position: absolute; right: 0%"
        width="100%"
      >
        <!-- config nav -->

        <v-flex v-if="e1 == 1" class="text-right">
          <v-btn
            :disabled="!isConfigComplete"
            color="primary"
            @click="[sendChanges(), (e1 = 2)]"
            class="ma-5"
          >
            <!-- <translate>Continue</translate> -->
            Continue
          </v-btn>
        </v-flex>


        <!-- metadata nav -->

            <v-flex v-if="e1 == 2" class="text-right">
                <v-btn outlined @click="e1 = 1">
                <!-- <translate>Back</translate> -->
                    Back
                </v-btn>

                <v-btn color="primary" @click="e1 = 3" class="ma-5">
                <!-- <translate>Continue</translate> -->
                    Continue
                </v-btn>
            </v-flex>

        <!-- publish nav -->
        <v-flex v-if="e1 == 3" class="d-flex mb-6">
          <v-btn
            outlined
            color="warning"
            @click="archiveProject(project.researchIndex)"
            class="mr-auto ma-5"
          >
            <!-- <translate>Delete</translate> -->
            Archive
          </v-btn>
          <v-flex class="text-right">
            <v-btn outlined @click="e1 = 2" class="">
              <!--  <translate>Back</translate> -->
              Back
            </v-btn>

            <v-btn
              :disabled="publishInProgress"
              color="success"
              @click="publishProject"
              class="ma-5"
            >
              <translate v-if="publishInProgress">In progress...</translate>
              <!-- <translate v-else>Publish</translate> -->
              Publish
            </v-btn>
          </v-flex>
        </v-flex>
      </v-sheet>

      <!-- / Stepper buttons-->
    </v-stepper>
  </div>
</template>

<style>
.v-stepper__header {
  padding-bottom: 1px;
  border-bottom: 1px solid #ccc;
  background-color: #fafafa;
}
</style>

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
      e1: 1,
      changes: {},
      publishInProgress: false,
      researchName: this.project.researchname,
    };
  },
  computed: {
    ...mapGetters({
      modifiedExport: "getModifiedExport",
      modifiedImport: "getModifiedImport",
      modifiedTitle: "getModifiedWorkingTitle",
      modifiedFilePath: "getModifiedFilePath",
    }),
    isConfigComplete() {
      return this.hasFolder && this.hasService && this.hasTitle;
    },
    hasFolder() {
      if (this.modifiedFilePath.length > 0) {
        return true
      }
      try {
      if (this.project.portIn[0]["properties"]["customProperties"]["filepath"] !== undefined) {
        return true;
      }}
      catch (e) {
        return false
      }
      return false
    },
    hasService() {
      if (this.modifiedExport.length !== 0) {
        if (this.modifiedExport.remove.length > this.modifiedExport.add.length) {
          return false
        }
      }
      else if (this.project.portOut.length === 0) {
        return false
      }
      return true
    },
    hasTitle() {
       return !!this.project.researchname || !!this.modifiedTitle.trim()
    },
  },
  props: ["project"],
  methods: {
    receiveChanges(pChanges) {
      this.changes = pChanges;
    },
    sendChanges() {
      if (this.project.researchname !== this.modifiedTitle) {
        this.$store.dispatch("changeResearchname", {
          researchIndex: this.project["researchIndex"],
          researchname: this.modifiedTitle,
        });
        //this.project.researchname = this.researchName;
      }

      if (Object.keys(this.changes).length > 0) {
        this.$store.dispatch("changePorts", this.changes);
        this.changes = {};
      }
    },
    archiveProject(rId) {
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
            text = this.$gettext("Your project was successfully published.");
          } else {
            this.publishInProgress = false;
          }

          this.$root.$emit("showsnackbar", text);
        }
      );
    },
  },
};
</script>

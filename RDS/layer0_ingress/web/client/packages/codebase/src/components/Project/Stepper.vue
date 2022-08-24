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

        <v-stepper-step step="3"
          ><translate>Publish</translate>
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
              @changeResearchname="receiveResearchname"
            />
          </v-card>
        </v-stepper-content>

        <!-- Step 2: Metadata -->
        <v-stepper-content step="2">
          <v-card
            v-if="e1 == 2"
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
        Folder:
        {{ project.currentFilePath }}
        {{ modifiedFilePath }}
        Name:
        {{ researchName }}
        {{ modifiedTitle }}
        Service:
        {{ project.portOut }}
        {{ modifiedExport }}
        isCompleted:
        {{ isConfigComplete }}

        <v-flex v-if="e1 == 1" class="text-right">
          <v-btn
            :disabled="isConfigComplete()"
            color="primary"
            @click="[sendChanges(), (e1 = 2)]"
            class="ma-5"
          >
            <!-- <translate>Continue</translate> -->
            Continue >
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
            color="error"
            @click="archiveProject(project.researchIndex)"
            class="mr-auto ma-5"
          >
            <!-- <translate>Delete</translate> -->
            Delete
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
      configurationLockState: true,
      publishInProgress: false,
      researchName: this.project.researchname,
      currentFilePath:
        this.project.portIn[0]?.properties?.customProperties?.filepath,
    };
  },
  computed: {
    ...mapGetters({
      modifiedExport: "getModifiedExport",
      modifiedTitle: "getModifiedWorkingTitle",
      modifiedFilePath: "getModifiedFilePath",
    }),
    isConfigComplete() {
      return this.hasFolder() && this.hasService() && this.hasTitle;
    },
  },
  props: ["project"],
  beforeMount() {
    if (this.isConfigComplete()) {
      this.e1 = 2;
    }

    this.configurationLockState = this.getInitialConfigurationLockState();
  },
  methods: {
    hasFolder() {
      if (!!this.modifiedFilePath) {
        return !!this.modifiedFilePath;
      }
      return this.currentFilePath === undefined
        ? false
        : this.currentFilePath.length > 0
        ? true
        : false;
    },
    hasService() {
      return !!this.project.portOut.length || !!this.modifiedExport.length;
    },
    hasTitle() {
      // TODO
      // check for whitespaces (.trim())
      return !!this.project.researchname.length || !!this.modifiedTitle.length;
    },
    isConfigComplete() {
      return this.hasFolder() && this.hasService() && this.hasTitle();
    },
    receiveResearchname(researchname) {
      this.researchName = researchname;
    },
    getInitialConfigurationLockState() {
      if (!!this.project["portOut"] && !!this.project["portIn"]) {
        return false;
      }
      return true;
    },
    setConfigurationLock(pChanges) {
      let numberOfSelectedPorts =
        this.project.portOut.length +
        pChanges["export"]["add"].length -
        pChanges["export"]["remove"].length;
      if (numberOfSelectedPorts !== 0) {
        if (!!this.changes["import"]["add"]) {
          for (let i of this.changes["import"]["add"]) {
            if (!i["filepath"]) {
              return true;
            }
          }
        }
        return false;
      } else {
        return true;
      }
    },
    receiveChanges(pChanges) {
      this.changes = pChanges;
      this.configurationLockState = this.setConfigurationLock(pChanges);
    },
    sendChanges() {
      if (this.project.researchname !== this.researchName) {
        this.$store.dispatch("changeResearchname", {
          researchIndex: this.project["researchIndex"],
          researchname: this.researchName,
        });
        this.project.researchname = this.researchName;
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

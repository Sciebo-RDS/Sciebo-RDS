<template>
  <v-stepper v-model="e1" alt-labels>
    <v-stepper-header>
      <v-stepper-step :complete="e1 > 1" step="1">
        <translate>Configuration</translate>
      </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step :complete="e1 > 2" step="2">
        <translate>Metadata</translate>
      </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step step="3"><translate>Publish</translate> </v-stepper-step>
    </v-stepper-header>

    <v-stepper-items>
      <v-stepper-content step="1">
        <v-card class="mb-12" height="auto" flat>
          <StepConfiguration
            :project="project"
            @changePorts="receiveChanges"
            @changeResearchname="receiveResearchname"
          />
        </v-card>

        <v-btn text disabled> <translate>Back</translate> </v-btn>

        <v-btn :disabled="configurationLockState" color="primary" @click="[sendChanges(), (e1 = 2)]">
          <translate>Continue</translate>
        </v-btn>
      </v-stepper-content>

      <v-stepper-content step="2">
        <v-card
          v-if="e1 == 2"
          class="d-flex flex-column justify-center mb-12"
          min-height="500px"
        >
          <StepMetadataEditor :project="project" />
        </v-card>

        <v-btn text @click="e1 = 1">
          <translate>Back</translate>
        </v-btn>

        <v-btn color="primary" @click="e1 = 3">
          <translate>Continue</translate>
        </v-btn>
      </v-stepper-content>

      <v-stepper-content step="3">
        <v-card class="mb-12" height="auto" flat>
          <StepPublish :project="project" />
        </v-card>

        <v-btn text @click="e1 = 2">
          <translate>Back</translate>
        </v-btn>

        <v-btn :disabled="publishInProgress" color="success" @click="publishProject">
          <translate v-if="publishInProgress">In progress...</translate>
          <translate v-else>Publish</translate>
        </v-btn>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<style scoped>
/*.v-stepper__header {
  box-shadow: none;
} 
.v-stepper {
  box-shadow: none;
}*/
</style>

<script>
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
    };
  },
  props: ["project"],
  beforeMount() {
    if (this.project.status > 1) {
      this.e1 = 2;
    }

    this.configurationLockState = this.getInitialConfigurationLockState();
  },
  methods: {
    receiveResearchname(researchname) {
      this.researchName = researchname;
    },
    getInitialConfigurationLockState() {
      if (!!this.project.portOut.length && !!this.project["portIn"]) {
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
    alert(msg) {
      alert(msg);
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
    publishProject() {
      this.publishInProgress = true;

      this.$root.$emit(
        "showsnackbar",
        this.$gettext(
          "The publishing process will be executed now. We will inform you, when finished or something goes wrong."
        )
      );

      this.$socket.client.emit(
        "triggerSynchronization",
        {
          researchIndex: this.project["researchIndex"],
        },
        (result) => {
          let text = this.$gettext(
            "There was an error, while we publish your project. Please check, if you have enter all fields in metadata step."
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

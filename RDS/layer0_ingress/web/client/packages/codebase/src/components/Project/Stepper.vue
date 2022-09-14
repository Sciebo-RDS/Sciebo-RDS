<template>
  <div style="height: 100%">
    <v-stepper v-model="e1" alt-labels flat style="height: 100%">
      <!-- Stepper header -->
      <v-stepper-header 
      style="
      box-shadow: none !important;
      padding-bottom: 1px;
      border-bottom: 1px solid #ccc;
      background-color: #fafafa;">
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
        style="bottom: 0%; position: absolute; right: 0%; border-top: 1px solid #ccc!important"
        width="100%"
      >
        <!-- config nav -->
        <v-flex v-if="e1 == 1" class="d-flex mb-6">
          <v-btn
            outlined
            color="error"
            @click="archiveProject(loadedProject.researchIndex)"
            class="mr-auto ma-5"
          >
            <!-- <translate>Delete</translate> -->
            Delete
          </v-btn>
          <v-flex class="text-right">
            

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
              :disabled="publishInProgress"
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
   /*    changes: {}, */
      publishInProgress: false,
      researchName: this.project.researchname,
    };
  },
  computed: {
    ...mapGetters({
      loadedTitle: "getLoadedResearchName",
      loadedProject: "getLoadedProject",
      loadedFilePath: "getLoadedFilePath",
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
       return !!this.loadedTitle || !!this.originalResearchName;
    },
    portChanges() {
      let changes = this.computePortChanges()
      return changes 
    }
  },
  props: ["project", "e1"],
  methods: {
    /* receiveChanges(pChanges) {
      this.changes = pChanges;
    }, */
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
          remove: originalPortOutNames.filter(p => !loadedPortOutNames.includes(p)),
          change: []
        }
      }

    },
    sendChanges() {
      if (this.originalResearchName !== this.loadedTitle) {
        this.$store.dispatch("changeResearchname", {
          researchIndex: this.loadedProject["researchIndex"],
          researchname: this.loadedTitle,
        });
      }
      console.log(JSON.stringify(this.portChanges))
        this.$store.dispatch("changePorts", this.portChanges);
        /* this.changes = {}; */
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

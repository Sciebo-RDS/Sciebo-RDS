<template>
  <v-container>
    <v-row>
      <v-col class="mx-auto" cols="12" md="10" lg="10" justify="center">
        <v-card flat >
          <v-card-title v-translate class="justify-center" align="center">
            Publish your project
          </v-card-title>
          <v-card-subtitle v-if="!published && !publishInProgress && fileUploadMessages.length == 0" class="mt-2">
            Make sure these settings are correct!
          </v-card-subtitle>
          <v-card-text>
            <p v-if="!published && !publishInProgress && fileUploadMessages.length == 0" class="my-5">
              Your <span class="text-decoration-underline">{{displayNamePortIn}}</span> project folder <span class="font-weight-bold" style="font-family: monospace;">{{loadedFilePath}}</span> will be published to <span class="text-decoration-underline">{{displayNamePortOut}}</span>.
            
              <v-row class="my-5 justify-center" style="align-items:center">
              <v-col
                  cols="3">
                <v-img :src="iconPortIn" />
              </v-col>
              <v-col cols="2">
                <p style="font-size: 2em; text-align: center;">
                  &#10230;
                </p>
              </v-col>
              <v-col cols="3">
                <v-img :src="iconPortOut" />
              </v-col>
            </v-row>
            </p>
            <p v-else class="my-10 text-left">

              <!-- publishing Steps -->
              <p v-if="fileUploadMessages.length > 0">
                  <v-row v-for="value in fileUploadMessages" :key="value.message">
                    <v-col cols="1">
                      <v-icon>{{ getIconByType(value.type) }}</v-icon>

                    </v-col>
                    <v-col cols="11">
                      {{ value.message }}
                    </v-col>
                </v-row>
              </p>
              <v-row v-if="publishInProgress">
                    <v-col cols="1">
                      <v-progress-circular
                        indeterminate
                        color="primary"
                      ></v-progress-circular>

                    </v-col>
                    <v-col cols="11">
                      Publishing to {{ displayNamePortOut  }}...
                    </v-col>
                </v-row>

              <!-- publishing Success -->
              <v-row v-if="published">
                <v-col cols="1">
                  <v-icon color="success">
                    mdi-check-circle
                  </v-icon>
                </v-col>
                <v-col cols="11">
                  Project <span class="font-weight-bold">{{loadedResearchName}}</span> was successfully published to {{displayNamePortOut}}.
                </v-col>
              </v-row>
            </p>

          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>


<script>
import { mapGetters } from "vuex";

export default {
  props: ["project", "published", "publishInProgress"],
  data() {
    return {
      publishingSteps: []
    };
  },
  computed: {
    ...mapGetters({
      loadedPortIn: "getLoadedPortIn",
      loadedPortOut: "getLoadedPortOut",
      userServiceList: "getUserServiceList",
      loadedFilePath: "getLoadedFilePath",
      loadedResearchName: "getLoadedResearchName",
      getMessagesByResearchIndex: "getMessagesByResearchIndex",
      getIconByType: "getIconByType",
    }),

    serviceIn() {
      try {
        return this.userServiceList.filter(s => s.servicename === this.loadedPortIn[0].port)[0];
      } catch (e) {
        return null;
      }
    },
    displayNamePortIn() {
      try {
        return this.serviceIn["displayName"];
      } catch (e) {
        return "";
      }
    },
    iconPortIn() {
      try {
        return this.serviceIn["icon"];
      } catch (e) {
        return "";
      }
    },
    serviceOut() {
      try {
        return this.userServiceList.filter(s => s.servicename === this.loadedPortOut[0].port)[0];
      } catch (e) {
        return null;
      }
    },
    displayNamePortOut() {
      try {
        return this.serviceOut["displayName"];
      } catch (e) {
        return "";
      }
    },
    iconPortOut() {
      try {
        return this.serviceOut["icon"];
      } catch (e) {
        return "";
      }
    },
    fileUploadMessages() {
      return this.getMessagesByResearchIndex(this.project.researchIndex);
    }
  },
};
</script>

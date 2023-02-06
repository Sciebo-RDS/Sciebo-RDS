<template>
  <v-container>
    <v-row>
      <v-col class="mx-auto" cols="12" md="10" lg="10" justify="center" align="center">
        <v-card flat >
          <v-card-title v-translate class="justify-center">
            Publish your project
          </v-card-title>
          <v-card-subtitle v-if="!published" class="mt-2">
            Make sure these settings are correct!
          </v-card-subtitle>
          <v-card-text>
            <p v-if="!published" class="my-10"> Your <span class="text-decoration-underline">{{displayNamePortIn}}</span> project folder <span class="font-weight-bold" style="font-family: monospace;">{{loadedFilePath}}</span> will be published to <span class="text-decoration-underline">{{displayNamePortOut}}</span>. </p>
            <p v-else class="my-10 text-left">
              <v-row>
                <v-col cols="1">
                  <v-icon color="success">
                    mdi-check-circle
                  </v-icon>
                </v-col>
                <v-col cols="11">
                  Project <span class="font-weight-bold">{{loadedResearchName}}</span> was successfully published to {{displayNamePortOut}}. <br/>
                  Folder: <span class="font-weight-bold" style="font-family: monospace;">{{loadedFilePath}}</span>
                </v-col>
              </v-row>
            </p>

            <v-row class="my-2" justify="center" align="center">
              <v-col
                  cols="3">
                <v-img :src="iconPortIn" style="outline-offset: 5px;outline: 1px solid #000;outline-radius: 0%;" />
              </v-col>
              <v-col cols="2">
                <p style="font-size: 2em;">
                  &#10230;
                </p>
              </v-col>
              <v-col cols="3">
                <v-img :src="iconPortOut" style="outline-offset: 5px;outline: 1px solid #000;outline-radius: 0%;" />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>


<script>
import { mapGetters } from "vuex";

export default {
  props: ["project", "published"],
  computed: {
    ...mapGetters({
      loadedPortIn: "getLoadedPortIn",
      loadedPortOut: "getLoadedPortOut",
      userServiceList: "getUserServiceList",
      loadedFilePath: "getLoadedFilePath",
      loadedResearchName: "getLoadedResearchName",
    }),

    serviceIn() {
      console.log("1");
      console.log(this.userServiceList); // OK! -> OSF + ownCloud drin
      console.log(this.loadedPortIn); // EMPTY! -> port-owncloud-sciebords-uni-muenster-de sollte sein

      if (this.loadedPortIn.length !== 0) {
        return this.userServiceList.filter(s => s.servicename === this.loadedPortIn[0].port)[0];
      }
      return null;
    },
    displayNamePortIn() {
      return this.serviceIn["displayName"];
    },
    iconPortIn() {
      return this.serviceIn["icon"];
    },
    serviceOut() {
      console.log("2");
      console.log(this.userServiceList);
      console.log(this.loadedPortOut);

      if (this.loadedPortOut.length !== 0) {
        return this.userServiceList.filter(s => s.servicename === this.loadedPortOut[0].port)[0];
      }
      return null;
    },
    displayNamePortOut() {
      return this.serviceOut["displayName"];
    },
    iconPortOut() {
      return this.serviceOut["icon"];
    }

  },
};
</script>

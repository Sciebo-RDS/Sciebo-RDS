<template>
    <v-container>
      <v-row>
        <v-card width="400" outlined>
          
          <v-card-text>
            <div></div>
            <p class="text-h6 text--primary pb-3" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" :title="project.researchname">
                {{ project.researchname}}
                <v-divider class="my-2"></v-divider>
            </p>
            <v-div class="">

              <!-- Repository name-->
              <v-row class="d-flex mx-1" flat  tile>
                <v-col class="py-1" justify="left" flat tile>
                  Repository:
                </v-col>

                <v-col class="py-1" justify="right" flat tile>
                  {{ !!displayNamePortOut ? displayNamePortOut : "N/A"}}
                </v-col>
              </v-row>

              <!-- Repository Project-ID-->
              <v-row class="d-flex mx-1" flat  tile>
                <v-col class="py-1" justify="left" flat tile>
                  Repository-ID:
                </v-col>

                <v-col class="py-1" justify="right" flat tile>
                  {{ !!project.portOut[0].properties.customProperties.projectId ? project.portOut[0].properties.customProperties.projectId : "N/A"}}
                </v-col>
              </v-row>

              <!-- DOI-->
              <v-row class="d-flex mx-1" flat  tile>
                <v-col class="py-1" justify="left" flat tile>
                  Identifier (DOI):
                </v-col>

                <v-col class="py-1" justify="right" flat tile>
                  {{ !!project.portOut[0].properties.customProperties.DOI ? project.portOut[0].properties.customProperties.DOI : "N/A"  }}
                </v-col>
              </v-row>


            </v-div>
          </v-card-text>
        <v-divider class="my-5"></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
    <!-- TODO: Add link mask for repositories to make linking possible -->
      <v-btn
        text
        color="teal accent-4"
        @click=""
        
      >
        Go to Publication
      </v-btn>
    </v-card-actions>
        </v-card>
      </v-row>
    </v-container>
</template>

<script>

export default({
  props: ["project"],
  computed: {
    displayNamePortOut() {
      try {
        return this.userServiceList.filter(s => s.servicename === this.loadedPortOut[0].port)[0].displayName;
      } catch (e) {
        return "";
      }
    },
  }
})
</script>

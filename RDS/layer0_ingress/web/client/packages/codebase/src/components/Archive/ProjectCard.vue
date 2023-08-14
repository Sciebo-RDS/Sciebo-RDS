<template>
    <v-container>
      <v-row justify="space-around">
        <v-card width="400" outlined>
          
          <v-card-text>
            <div></div>
            <p class="text-h6 text--primary pb-3">
                {{ project.researchname}}
            </p>
            <v-div class="">
            <v-row class="d-flex" flat  tile>
              <v-col class="flex-grow-0 flex-shrink-1 py-0" flat tile>
                Repository-ID:
              </v-col>

              <v-col class="ml-5 flex-grow-1 flex-shrink-0 py-0" flat tile>
                {{ !!project.portOut[0].properties.customProperties.projectId ? project.portOut[0].customProperties.projectId : "N/A"}}
              </v-col>

            </v-row>
            <v-row class="d-flex" flat  tile>
              <v-col class="flex-grow-0 flex-shrink-1 py-0" flat tile>
                Identifier (DOI):
              </v-col>

              <v-col class="ml-5 flex-grow-1 flex-shrink-0 py-0" flat tile>
                {{ !!project.portOut[0].properties.customProperties.DOI ? project.portOut[0].properties.customProperties.DOI : "N/A"  }}
              </v-col>

            </v-row>
            </v-div>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
    <!-- TODO: Add link mask for repositories to make linking possible -->
      <v-btn
        text
        color="teal accent-4"
        @click=""
        
      >
        Got to Publication
      </v-btn>
    </v-card-actions>
        </v-card>
      </v-row>
    </v-container>
</template>

<script>

export default({
    props: ["project"],

})
</script>

<template>
  <v-card width="400" class="ma-2" outlined>
    <v-card-text>
      <div class="caption">{{ project.portIn[0].properties.customProperties.filepath }}</div>
      <p class="text-h6 text--primary pb-3" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" :title="project.researchname">
          {{ project.researchname}}
          <v-divider class="my-2"></v-divider>
      </p>
      <v-div class="">


        <!-- Project Publishing Time-->
        <v-row class="d-flex" flat  tile>
          <v-col class="py-1 text--primary" justify="left" flat tile>
            Published:
          </v-col>

          <v-col class="py-1" justify="right" flat tile>
            {{ !!timePublishedMS ? timePublishedMS : "N/A"}}
          </v-col>
        </v-row>

        <!-- Repository name-->
        <v-row class="d-flex" flat  tile>
          <v-col class="py-1 text--primary" justify="left" flat tile>
            Repository:
          </v-col>

          <v-col class="py-1" justify="right" flat tile>
            {{ !!displayNamePortOut ? displayNamePortOut : "N/A"}}
          </v-col>
        </v-row>

        <!-- Repository Project-ID-->
        <v-row class="d-flex" flat  tile>
          <v-col class="py-1 text--primary" justify="left" flat tile>
            Repository-ID:
          </v-col>

          <v-col class="py-1" justify="right" flat tile>
            {{ !!project.portOut[0].properties.customProperties.projectId ? project.portOut[0].properties.customProperties.projectId : "N/A"}}
          </v-col>
        </v-row>

        <!-- DOI-->
        <v-row class="d-flex" flat  tile>
          <v-col class="py-1 text--primary" justify="left" flat tile>
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
    <!-- TODO: Implement this for all Repositories -->
      <a target="_blank" :href="!!projectLink && !!projectId ? projectLink : '#'">
      <v-btn
        text
        :color="!!projectLink ? 'teal accent-4' : 'grey lighten-2'"
        :disabled="!projectLink"
      >
        Go to Publication
      </v-btn>
      </a>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapState } from "vuex";

export default({
  props: ["project"],
  computed: {
    ...mapState({
      userservicelist: (state) => state.RDSStore.userservicelist,
    }),
    displayNamePortOut() {
      try {
        let fullPort = this.userservicelist.filter(s => s.servicename === this.project.portOut[0].port)[0];
        return fullPort.displayName;
      } catch (e) {
        return "";
      }
    },
    projectId() {
      return this.project.portOut[0].properties.customProperties.projectId;
    },
    projectLinkTemplate() {
      try {
        let fullPort = this.userservicelist.filter(s => s.servicename === this.project.portOut[0].port)[0];
        return fullPort.projectLinkTemplate;
      } catch (e) {
        return "";
      }
    },
    projectLink() {
      try {
        let projectLink = new Function("return `" + this.projectLinkTemplate + "`").call(this.projectLinkTemplate);
        return projectLink;
      } catch (e) {
        return "";
      }
    },
    timePublishedMS() {
      return !!this.project.portOut[0].properties.customProperties.timePublishedS ?  this.formatTime(this.project.portOut[0].properties.customProperties.timePublishedS) : "";
    }
  },
  methods: {
    formatTime(ts) {
      return new Date(ts * 1000).toLocaleString(navigator.language, {hourCycle: "h24", dateStyle: "medium", timeStyle: "short"})
    }
  }
})
</script>

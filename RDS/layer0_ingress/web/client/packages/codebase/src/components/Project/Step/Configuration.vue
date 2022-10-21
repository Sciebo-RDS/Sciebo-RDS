<template>
  <v-container>
    <v-row>
      <v-col class="mx-auto" cols="11">
        <!-- <v-col class="mx-auto" cols="12" md="10" lg="10" xl="8"> -->
        <v-card flat>
          <v-card-title class="justify-center" :class="[originalResearchName ? '' : 'font-italic']">
            {{ originalResearchName ? originalResearchName : 'New Project ' }}
          </v-card-title>

          <configuration-folder :project="project"/>
          <v-divider />
          <configuration-research-name />
          <v-divider />
          <configuration-service/>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import ConfigurationFolder from "./Configuration.Folder.vue";
import ConfigurationResearchName from "./Configuration.ResearchName.vue";
import ConfigurationService from "./Configuration.Service.vue";

export default {
  components: { ConfigurationFolder, ConfigurationResearchName, ConfigurationService },
  data: () => ({
    selectedPorts: [],
    currentFilePath: "",
    workingTitle: "",
  }),
  computed: {
    ...mapGetters({
      ports: "getUserServiceList",
      ownCloudServicename: "getOwnCloudServername",
      allProjects: "getProjectlist",
      loadedProject: "getLoadedProject",
      originalResearchName: "getOriginalResearchNameForLoadedProject"
    }),
  },
  props: ["project"],
};
</script>

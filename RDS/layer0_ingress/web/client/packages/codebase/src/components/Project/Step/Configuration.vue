<template>
  <v-container>
    <v-row>
      <v-col class="mx-auto" cols="11">
        <!-- <v-col class="mx-auto" cols="12" md="10" lg="10" xl="8"> -->
        <v-card flat>
          <v-card-title class="justify-center">
            {{ originalResearchName ? originalResearchName : 'Project ' + (loadedProject.researchId+1) }}
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
  beforeMount() {
/*     function portHas(ports, servicename) {
      for (const port of ports) {
        if (port.port === servicename) {
          return true;
        }
      }
      return false;
    }

    this.userPorts = this.selectedPorts = this.ports.filter((port) =>
      portHas(this.project.portOut, port.servicename)
    );

    this.workingTitle = this.project.researchname;

    this.currentFilePath = this.filepath(this.project); */
/* 
    window.addEventListener("message", this.eventloop); */
/*     if (!this.project.portIn.length) {
      this.emitChanges();
    } */
  },
/*   beforeDestroy() {
    window.removeEventListener("message", this.eventloop);
  }, */
  methods: {
    /* eventloop(event) {
      if (event.data.length > 0) {
        var payload = JSON.parse(event.data);
        switch (payload.event) {
          case "filePathSelected":
            let data = payload.data;
            if (data.projectId == this.project.projectId) {
              this.currentFilePath = data.filePath;
              console.log(
                "setModifiedFilePath: " +
                  this.currentFilePath +
                  " configuration.vue"
              );
              //this.$store.commit("setModifiedFilePath", this.currentFilePath);
            }
            break;
        }
      }
    },
    computeChanges() {
      let strippedRemoveOut = this.computeStrippedOut(this.computeRemoveOut());
      let strippedAddOut = this.computeStrippedOut(this.computeAddOut());
      let importAdd = this.setImportAdd();
      let changes = {
        researchIndex: this.project["researchIndex"],
        import: {
          add: importAdd,
          remove: [],
          change: [],
        },
        export: {
          add: strippedAddOut,
          remove: strippedRemoveOut,
          change: [],
        },
      };

      if (this.workingTitle !== this.project.researchname) {
        changes["researchname"] = this.workingTitle;
      }

      return changes;
    },
    computeRemoveOut() {
      return this.userPorts.filter((i) => !this.selectedPorts.includes(i));
    },
    computeAddOut() {
      return this.selectedPorts.filter((i) => !this.userPorts.includes(i));
    },
    computeStrippedOut(pOut) {
      let strippedOut = [];
      for (let i of pOut) {
        strippedOut.push({ servicename: i.servicename });
      }
      return strippedOut;
    },
    setImportAdd() {
      let add = [];
      if (this.project.portIn.length == 0) {
        return [
          {
            servicename: "port-owncloud-" + this.ownCloudServicename,
            filepath: this.currentFilePath,
          },
        ];
      }
      for (let i of this.project["portIn"]) {
        if (!!this.currentFilePath) {
          add = [
            {
              servicename: i["port"],
              filepath: this.currentFilePath,
            },
          ];
        }
      }
      return add;
    }, */
    emitChanges() {
      let payload = this.computeChanges();
      this.$emit("changePorts", payload);
      this.changes = {};
    },
    /* filepath(project) {
      if (!project.portIn.length) {
        return "";
      }
      const service = this.getService(
        project.portIn,
        "port-owncloud-" + this.ownCloudServicename
      );
      if (service !== undefined) {
        return service.properties.customProperties.filepath;
      }

      return this.currentFilePath;
    }, */
  },
  props: ["project"],
};
</script>

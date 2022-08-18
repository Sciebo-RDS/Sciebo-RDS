<template>
  <v-container>
      <v-row>
        <v-col class="mx-auto" cols="11">
          <!-- <v-col class="mx-auto" cols="12" md="10" lg="10" xl="8"> -->
        <v-card flat>
      <v-card-title class="justify-center" v-translate>Configure your Project</v-card-title>
      <!--<v-card-subtitle>Please select the services you want to publish to: </v-card-subtitle>-->

            <configuration-folder :project="project" :currentFilePath="currentFilePath"/>
                <v-divider/>
            <configuration-title  :project="project" />
                <v-divider/>
            <configuration-service  :project="project" :currentFilePath="currentFilePath"/>
    </v-card>
            </v-col>
        </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import ConfigurationFolder from './Configuration.Folder.vue';
import ConfigurationTitle from './Configuration.Title.vue';
import ConfigurationService from './Configuration.Service.vue';

export default {
  components: { ConfigurationFolder, ConfigurationTitle, ConfigurationService },
  data: () => ({
    selectedPorts: [],
    currentFilePath: "",
    workingTitle: "",
    configStep: 0,
  }),
  computed: {
    ...mapGetters({
      ports: "getUserServiceList",
      ownCloudServicename: "getOwnCloudServername",
      modifiedProject: "getModifiedProject",
      modifiedWorkingTitle: "getModifiedWorkingTitle",
    }),
  },
  beforeMount() {
    function portHas(ports, servicename) {
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

    this.currentFilePath = this.filepath(this.project);

    window.addEventListener("message", this.eventloop);
    if (!this.project.portIn.length) {
      this.emitChanges();
    }
    this.$store.commit('setModifiedResearchIndex', this.project["researchIndex"])
  },
  beforeDestroy() {
    window.removeEventListener("message", this.eventloop);
    this.$store.commit('setModifiedResearchIndex', null)
  },
  methods: {
    eventloop(event) {
      if (event.data.length > 0) {
        var payload = JSON.parse(event.data);
        switch (payload.event) {
          case "filePathSelected":
            let data = payload.data;
            if (data.projectId == this.project.projectId) {
              this.currentFilePath = data.filePath;
              this.emitChanges();
            }
            break;
        }
      }
    },/* 
    togglePicker() {
      this.showFilePicker(this.project.projectId, this.currentFilePath);
    }, */
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
    },
    emitChanges() {
      let payload = this.computeChanges();
      this.$emit("changePorts", payload);
      this.changes = {};
    },
    filepath(project) {
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
    },
  },
  props: ["project"],
};
</script>

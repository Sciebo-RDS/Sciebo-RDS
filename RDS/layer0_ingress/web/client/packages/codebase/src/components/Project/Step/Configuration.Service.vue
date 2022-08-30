<template>
    <v-card
        flat>
        <v-list two line>
            <v-list-item class="">
                <v-list-item-avatar size="3em" class="align-self-start" >
                    <v-icon size="2em"  color="black" class="grey lighten-2 rounded-circle pa-16  my-8">
                        mdi-numeric-3
                    </v-icon>
                </v-list-item-avatar>

            <v-list-item-content>
                <v-list-item-title class="text-h6 pb-1 align-self-start text-wrap" style="line-height: 2em;">
                    <v-row justify="space-around">
                            <v-col cols="auto" class="mr-auto">
                                Choose a repository.
                            </v-col>
                            <v-col cols="auto" class="text-right">
                                <v-icon
                                    color="error"
                                    v-if="selectedPorts.length == 0">
                                        mdi-alert-circle-outline
                                </v-icon>
                                <v-icon
                                    color="success"
                                    class="outlined"
                                    v-else>
                                        mdi-check-circle-outline
                                </v-icon>
                            </v-col>
                        </v-row>
                </v-list-item-title>

                <v-list-item-subtitle class="py-1 text-wrap">
                    Choose the repository you want to publish your data to.
                </v-list-item-subtitle>

                <v-list-item-content>
                    <v-row class="ma-1">
                        <v-col
                            v-for="p in ports.filter((i) => i['implements'].includes('metadata'))"
                            :key="p"
                            cols="3"
                            class="col-lg-2"
                            @click="setProfile(p)"
                            :style="selectedPorts.length > 0 && (selectedPorts[0].servicename == p.servicename) ? 'border: 1px solid black; max-width: 100%' : 'border: 1px solid transparent'"
                            align="center"
                            style="display: grid; align-content: end; align: center">

                            <v-img
                                :src="p.icon"
                                :style="(selectedPorts.length > 0 && selectedPorts[0].servicename == p.servicename) ? '' : 'opacity: 0.3'"/>
                            <small style="vertical-align: bottom">
                                {{ p['displayName'] }}
                            </small>
                        </v-col>
                    </v-row>
                </v-list-item-content>
            </v-list-item-content>
          </v-list-item>
        </v-list>
    </v-card>
</template>

// TODO: refactor variable names

<script>
import { mapGetters } from "vuex";

export default ({
    data() {
        return {
            selectedPorts: [],
        }

    },
    computed:{
        ...mapGetters({
        ports: "getUserServiceList",
        modifiedProject: "getModifiedProject",
        modifiedExport: "getModifiedExport"
        })
    },
    beforeMount() {
        function portHas(ports, servicename){
            for (const port of ports) {
                if (port.port === servicename) {
                    return true
                }
            }
            return false
        }
        this.userPorts = this.selectedPorts = this.ports.filter((port) =>
        portHas(this.project.portOut, port.servicename)
        )
    },
    methods: {
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
        setProfile(port) {
            if (this.selectedPorts.includes(port)){
                this.selectedPorts = []
            }
            else {
                this.selectedPorts = [port];
            }
            let strippedRemoveOut = this.computeStrippedOut(this.computeRemoveOut());
            let strippedAddOut = this.computeStrippedOut(this.computeAddOut());
            let importAdd = this.setImportAdd();
            this.$store.commit("setModifiedImport", {
                add: importAdd,
                remove: [],
                change: [],
                })
            this.$store.commit("setModifiedExport", {
                add: strippedAddOut,
                remove: strippedRemoveOut,
                change: [],
            })
        },
    },
    // TODO: Assure that currentFilePath in changes object is always up to date and that
    // updates in Filepicker are actually committet. Might be race condition, if filepath and 
    // in port are updated at the same time, but outport uses old filepath to update.
    // Better: make filepath and inport descrete
    props: ["project", "currentFilePath"],
})
</script>

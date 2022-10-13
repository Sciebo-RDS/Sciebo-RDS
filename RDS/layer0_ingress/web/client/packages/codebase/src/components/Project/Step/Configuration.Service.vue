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
                                    v-if="loadedPortOut.length == 0">
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
                            :key="p.client_id"
                            cols="3"
                            class="col-lg-2"
                            @click="selectPort(p)"
                            :style="isSelected(p) ? selectedStyle() : 'border: 1px solid transparent'"
                            align="center"
                            style="display: grid; align-content: end; align: center">
                            <v-img
                                :src="p.icon"
                                :style="isSelected(p) ? '' : 'opacity: 0.3'"/>
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
        loadedFilePath: "getLoadedFilePath",
        originalPortOut: "getOriginalPortOutForLoadedProject",
        changedPorts: "getChangedPorts"
        }),
        loadedPortIn: {
            get() {
                return this.$store.getters.getLoadedPortIn
            },
            set(value) {
                this.$store.commit('setLoadedPortIn', value)
            }
        },
        loadedPortOut: {
            get() {
                return this.$store.getters.getLoadedPortOut
            },
            set(value) {
                this.$store.commit('setLoadedPortOut', value)
            }
        },
    },
    beforeMount() {
        this.userPorts = this.selectedPorts = this.ports.filter((port) => {
                for (const p of this.loadedPortOut) {
                    if (p.port === port.servicename)
                    return true
                }
                return false
            }
        )
    },
    methods: {
        isSelected(p) {
            for (const s of this.loadedPortOut){
                if (s.port === p.servicename)
                    return true
            }
            return false
        },
         selectPort(port) {
            if (this.isSelected(port)) {
                return this.loadedPortOut = this.loadedPortOut.filter((p) => p.port !== port.servicename)
            }
            for (const oP of this.originalPortOut){
                if (oP.port == port.servicename) {
                    return this.loadedPortOut = this.originalPortOut.filter((p) => p.port === port.servicename)
                }
            }
            return this.loadedPortOut = [...this.loadedPortOut, ({"port": port.servicename, type: ["metadata"]})]
         },
        selectedStyle() {
            if (this.$vuetify.theme.dark === true) {
                return 'border: 1px solid #bada55; max-width: 100%'
            }
            return 'border: 1px solid black; max-width: 100%'
        }

    },
})
</script>

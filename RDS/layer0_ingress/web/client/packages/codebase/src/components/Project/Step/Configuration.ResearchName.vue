<template>
    <v-card flat class="">
        <v-list two line>
            <v-list-item class="">
                <v-list-item-avatar size="3em" class="align-self-start" >
                    <v-icon size="2em"  color="black" class="grey lighten-2 rounded-circle pa-16  my-8">
                        mdi-numeric-2
                    </v-icon>
                </v-list-item-avatar>

                <v-list-item-content>
                    <v-list-item-title class="text-h6 align-self-start text-wrap" style="line-height: 2em;">
                        
                        <v-row justify="space-around">
                            <v-col cols="auto" class="mr-auto">
                                Name your project.
                            </v-col>
                            <v-col cols="auto" class="text-right">
                                <v-icon
                                    color="error"
                                    v-if="!hasResearchName">
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
                    <v-list-item-subtitle class="py-2 pb-4 text-wrap">
                        Give your project a name to distinguish it from other projects.
                    </v-list-item-subtitle>
                        <v-text-field
                            outlined
                            :label="originalResearchName ? originalResearchName : 'e.g. cat photos'"
                            v-model="loadedResearchName"
                            @keydown.esc="loadedResearchName = ''"
                            />
                </v-list-item-content>
          </v-list-item>
        </v-list>
    </v-card>
</template>

<script>
import { mapGetters } from 'vuex'

export default{
    computed: {
        ...mapGetters({
            allProjects: "getProjectlist",
            originalResearchName: "getOriginalResearchNameForLoadedProject"
        }),
        loadedResearchName: {
            get() {
                return this.$store.getters.getLoadedResearchName
            },
            set(value) {
                this.$store.commit('setLoadedResearchName', value.trim())
            }
        },
        hasResearchName() {
            return !!this.loadedResearchName || !!this.originalResearchName
    },
    },
}
</script>
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
                                    v-if="!(project.researchname || workingTitle)">
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
                        Give your project a name, to distinguish it from other projects.
                    </v-list-item-subtitle>
                        <v-text-field
                            outlined
                            class=""
                            :label="project.researchname ? project.researchname : 'e.g. cat photos'"
                            v-model="workingTitle"
                            @keydown.esc="cancelTitleEdit"
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
        workingTitle: {
            get() {
                return this.$store.getters.getModifiedWorkingTitle
            },
            set(value) {
                this.$store.commit('setModifiedWorkingTitle', value)
            }
        },
    },
    methods: {
        clearModifiedTitle() {
            this.$store.commit('setModifiedWorkingTitle', null)
        },
        cancelTitleEdit() {
            this.clearModifiedTitle()
            workingTitle = null
        },
    },
    props: ["project"],
}
</script>
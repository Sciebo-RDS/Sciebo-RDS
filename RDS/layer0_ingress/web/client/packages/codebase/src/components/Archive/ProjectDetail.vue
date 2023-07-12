<template>
    <div>
        <v-sheet
                    flat
                    height="6.3em"
                    color="grey lighten-5"
                    style="border-bottom: 1px solid #ccc!important">
                    <v-container fill-height>
                        <v-row justify="center" class="overline ma-0 text-h5 mx-2">
                            {{!!project.researchname ? project.researchname : 'Project ' + (project.researchId+1)}}
                        </v-row>
                    </v-container>
                </v-sheet>
        <v-card flat class="overflow-y-auto pa-5" style="max-height: calc( 100vh - 7.9em )">
        <p>Projektname: {{project.researchname}}</p>
        <v-divider></v-divider>
        <p v-if="project.portOut[0].port == 'port-openscienceframework'">
            Publication ID:
                <a :href="'https://osf.io' + project.portOut[0].properties.customProperties.projectId" target="_blank">
                    {{ project.portOut[0].properties.customProperties.projectId }}
                </a> <br>
            Identifier (DOI): {{ !!project.portOut[0].properties.customProperties.DOI ? project.portOut[0].properties.customProperties.DOI : "N/A"  }}
        </p>
    </v-card>
    </div>
</template>

<script>

export default({
    props: ["project"],

})
</script>

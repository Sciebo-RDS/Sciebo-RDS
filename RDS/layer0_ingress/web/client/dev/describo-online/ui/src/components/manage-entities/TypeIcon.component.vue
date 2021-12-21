<template>
    <div>
        <i class="fas fa-fw" :class="types[type]" v-if="types[type]"></i>
    </div>
</template>

<script>
export default {
    props: {
        type: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            types: {
                ContactPoint: "fa-address-card",
                CreateAction: "fa-plus",
                CreativeWork: "fa-image",
                Country: "fa-flag",
                Dataset: "fa-folder",
                DataDownload: "fa-download",
                File: "fa-file",
                GeoCoordinates: "fa-map-marker-alt",
                IndividualProduct: "fa-barcode",
                Language: "fa-sign-language",
                Organization: "fa-university",
                Person: "fa-user",
                Place: "fa-globe",
                PropertyValue: "fa-paragraph",
                Publication: "fa-newspaper",
                RepositoryCollection: "fa-cubes",
                RepositoryObject: "fa-cube",
                ScholarlyArticle: "fa-scroll",
                Script: "fa-code",
                SoftwareApplication: "fa-code",
                Workflow: "fa-project-diagram",
                WorkflowSketch: "fa-project-diagram",
            },
        };
    },
};
</script>

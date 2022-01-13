<template>
    <div class="box-card">
        <div class="flex flex-col space-y-2">
            <information-component type="info">
                Use the controls below to add entries into the collection so you can annotate them.
            </information-component>

            <file-browser-component
                :resource="resource"
                :root="folder"
                mode="openFile"
                :enable-file-selector="true"
                @selected-nodes="saveSelectedNodes"
            />
        </div>
    </div>
</template>

<script>
import FileBrowserComponent from "@/components/filebrowser/FileBrowser.component.vue";
import InformationComponent from "../Information.component.vue";

export default {
    components: {
        FileBrowserComponent,
        InformationComponent,
    },
    data() {
        return {
            resource: this.$store.state.target.resource,
            folder: this.$store.state.target.folder.path,
        };
    },
    methods: {
        async saveSelectedNodes(nodes) {
            try {
                await this.$http.post({ route: "/files", body: { files: nodes } });
            } catch (error) {
                console.log(error);
            }
        },
    },
};
</script>

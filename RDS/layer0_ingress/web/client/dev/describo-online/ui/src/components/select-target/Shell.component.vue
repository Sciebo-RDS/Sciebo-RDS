<template>
    <el-card class="box-card">
        <div slot="header" class="flex flex-row" v-if="!embeddedSession">
            <div class="flex flex-row" v-if="!target.resource && !target.folder">
                Select a resource to work with
                <div v-if="target.resource" class="ml-2">:&nbsp;{{ target.resource }}</div>
            </div>
            <div class="flex-grow"></div>
            <div v-if="target.resource">
                <el-button type="danger" size="small" @click="selectNewResourceAndTarget">
                    Change resource
                </el-button>
            </div>
        </div>
        <div class="flex flex-col">
            <div class="flex flex-row space-x-2" v-if="!target.resource && !embeddedSession">
                <onedrive-authenticator-component v-if="onedriveEnabled" />
                <owncloud-authenticator-component v-if="owncloudEnabled" />
            </div>

            <file-browser-component
                v-if="target.resource && !selectedFolder && !embeddedSession"
                class="m-4"
                :resource="target.resource"
                mode="openDirectory"
                :enable-file-selector="true"
                @selected-folder="setSelectedFolder"
            />
            <div class="flex flex-row" v-if="target.resource && target.folder">
                <div class="mr-2">Selected Resource:</div>
                <div>{{ target.resource }}:{{ target.folder.path }}</div>
                <div class="flex-grow"></div>
                <el-button
                    type="danger"
                    @click="selectNewTargetFolder"
                    size="small"
                    v-if="!embeddedSession"
                >
                    <i class="fas fa-trash"></i>
                </el-button>
            </div>
        </div>
    </el-card>
</template>

<script>
import HTTPService from "@/components/http.service";
import FileBrowserComponent from "@/components/filebrowser/FileBrowser.component.vue";

export default {
    components: {
        FileBrowserComponent,
    },
    data() {
        return {
            configuration: {},
            selectedFolder: undefined,
            embeddedSession: false,
        };
    },
    computed: {
        target: function() {
            if (this.$store.state.target.folder)
                this.selectedFolder = this.$store.state.target.folder;
            return this.$store.state.target;
        },
        owncloudEnabled: function() {
            return this.$store.state.configuration.services?.owncloud ? true : false;
        },
        onedriveEnabled: function() {
            return this.$store.state.configuration.services?.onedrive ? true : false;
        },
    },
    mounted() {
        this.setup();
    },
    methods: {
        async setup() {
            let httpService = new HTTPService({ $auth: this.$auth });
            let response = await httpService.get({ route: "/session" });
            if (response.status !== 200) {
                // do nothing
            }
            let { session, embeddedSession } = await response.json();
            this.embeddedSession = embeddedSession;
            if (this.embeddedSession) {
                let resource = Object.keys(session.services).pop();
                let folder = { path: session.services[resource].folder };
                if (resource && folder.path) {
                    this.selectedFolder = folder;
                    this.$store.commit("setTargetResource", { resource, folder });
                } else {
                    this.embeddedSession = false;
                }
            }
        },
        setSelectedFolder(folder) {
            this.selectedFolder = folder;
            this.$store.commit("setTargetResource", {
                resource: this.target.resource,
                folder,
            });
        },
        selectNewTargetFolder() {
            this.selectedFolder = undefined;
            this.$store.commit("setTargetResource", {
                resource: this.target.resource,
                folder: undefined,
            });
            this.$store.commit("setActiveCollection", {});
            this.$store.commit("setSelectedEntity", { id: "RootDataset" });
        },
        selectNewResourceAndTarget() {
            this.selectedFolder = undefined;
            this.$store.commit("setTargetResource", {
                resource: undefined,
                folder: undefined,
            });
            this.$store.commit("setActiveCollection", {});
            this.$store.commit("setSelectedEntity", { id: "RootDataset" });
        },
    },
};
</script>

<template>
    <div class="flex flex-row">
        <div class="flex flex-col w-full">
            <div class=" flex flex-col space-y-4 pb-2 border-b-2" v-if="enableFileSelector">
                <information-component type="warning" v-if="mode === 'openFile'">
                    You must expand each subfolder to load the child nodes. If you don't you'll only
                    get the folders.
                </information-component>
                <information-component type="info" v-if="mode === 'openDirectory'">
                    Select a folder to work with.
                </information-component>
                <information-component type="success" v-if="mode === 'openFile' && partsAdded">
                    The crate parts list has been updated.
                </information-component>
                <div v-if="mode === 'openFile'">
                    <el-checkbox v-model="selectAllChildren">
                        Select all children
                    </el-checkbox>
                </div>
            </div>
            <div class="overflow-scroll">
                <el-tree
                    v-loading="loading"
                    ref="tree"
                    :props="props"
                    node-key="path"
                    :load="loadNode"
                    :lazy="true"
                    :show-checkbox="enableFileSelector"
                    :check-strictly="!selectAllChildren"
                    :default-checked-keys="checkedNodes"
                    :default-expanded-keys="defaultExpandedKeys"
                    @check="handleNodeSelection"
                ></el-tree>
            </div>
        </div>
    </div>
</template>

<script>
import { flattenDeep, uniq, cloneDeep, uniqBy, compact, debounce } from "lodash";
import InformationComponent from "../Information.component.vue";

export default {
    components: {
        InformationComponent,
    },
    props: {
        resource: {
            type: String,
            required: true,
        },
        root: {
            type: String,
        },
        filterPaths: {
            type: Array,
            default: () => {
                return [];
            },
        },
        mode: {
            type: String,
            validator: (v) => ["openFile", "openDirectory"].includes(v),
            default: "openFile",
        },
        enableFileSelector: {
            type: Boolean,
            default: true,
        },
        checkedNodes: {
            type: Array,
        },
    },
    data() {
        return {
            filterFilePaths: [
                "ro-crate-metadata.json",
                "ro-crate-metadata.jsonld",
                "ro-crate-preview.html",
                ".DS_Store",
                ...this.filterPaths,
            ],
            debouncedAddParts: debounce(this.addParts, 1000),
            loading: false,
            partsAdded: false,
            selectAllChildren: false,
            data: [],
            httpService: undefined,
            props: {
                label: "path",
                children: "children",
                isLeaf: "isLeaf",
            },
            defaultExpandedKeys: [],
            selectedFolder: undefined,
        };
    },
    methods: {
        async loadNode(node, resolve) {
            this.loading = true;
            let content;
            if (node.level === 0) {
                await this.load({ resolve });
            } else if (node.level !== 0) {
                if (node.isLeaf) resolve();

                const path = node.data.parent
                    ? `${node.data.parent}/${node.data.path}`
                    : node.data.path;
                await this.load({ resolve, path });
            }
            this.loading = false;
        },
        async load({ resolve, path }) {
            let body = {
                resource: this.resource,
            };
            if (this.root && path) {
                body.path = path;
            } else if (this.root) {
                body.path = this.root;
            } else {
                body.path = path;
            }

            let response = await this.$http.post({
                route: "/folder/read",
                body,
            });
            if (response.status === 200) {
                let content = (await response.json()).content;
                content = content.map((e) => {
                    e.disabled = this.mode === "openDirectory" && e.isLeaf === true ? true : false;
                    return e;
                });
                content = content.filter((e) => {
                    return !this.filterFilePaths.includes(e.name);
                });
                resolve(content);
            } else if (response.status === 401) {
                // need to reauthenticate
                this.$log.error("need to authenticate");
                this.$notify({
                    title: "Error",
                    type: "error",
                    message: "Please log into onedrive",
                    showClose: false,
                    position: "top-left",
                });
                resolve([]);
            } else {
                // something else went wrong
                this.$notify({
                    title: "Error",
                    type: "error",
                    message: "There is an issue at this time.",
                    showClose: false,
                    position: "top-left",
                });
                resolve([]);
            }
        },
        async handleNodeSelection() {
            if (this.mode === "openDirectory") {
                this.loading = true;
                let node = this.$refs.tree.getCheckedNodes()[0];
                const path = node.parent ? `${node.parent}/${node.path}` : node.path;
                const id = node.id;
                this.$emit("selected-folder", { path: `/${path}`, id });
            } else {
                await this.debouncedAddParts();
            }
        },
        async addParts() {
            this.loading = true;
            this.partsAdded = false;
            await new Promise((resolve) => setTimeout(resolve, 100));
            let nodes = cloneDeep(this.$refs.tree.getCheckedNodes());
            nodes = nodes.map((n) => {
                n.parent = n.parent.replace(this.root, "");
                return n;
            });
            this.$emit("selected-nodes", nodes);
            this.loading = false;
            this.partsAdded = true;
            await new Promise((resolve) => setTimeout(resolve, 4000));
            this.partsAdded = false;
        },
    },
};
</script>

<style>
.el-tree-node__label {
    @apply text-lg;
}
.el-tree-node__content {
    @apply mb-1;
}
.is-disabled + .el-tree-node__label {
    @apply text-sm text-gray-400 cursor-not-allowed;
}
</style>

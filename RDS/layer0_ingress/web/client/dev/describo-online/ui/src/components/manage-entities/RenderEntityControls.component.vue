<template>
    <div>
        <div class="flex flex-row space-x-2 mb-4 p-2 bg-blue-200">
            <!-- navbar : controls -->
            <div>
                <el-button
                    @click="loadRootDataset"
                    size="small"
                    :disabled="entity && entity.eid === './'"
                >
                    Load Root Dataset
                </el-button>
            </div>
            <div>
                <el-button @click="showAddPropertyDialog" size="small">
                    <i class="fas fa-code"></i> Add Property
                </el-button>
            </div>
            <div class="flex flex-grow"></div>
            <div
                class="flex flex-row space-x-2 flex-grow"
                v-if="entity && entity.eid === './' && entityCount < maxEntitiesPerTemplate"
            >
                <el-input
                    v-model="crateName"
                    size="small"
                    placeholder="provide a name for the crate template"
                />
                <el-button @click="saveCrateAsTemplate" size="small" :disabled="!crateName">
                    <i class="fas fa-save"></i>
                    Save Crate as Template
                </el-button>
            </div>
            <div class="flex flex-rows space-x-1" v-if="entity && entity.eid !== './'">
                <div>
                    <el-button @click="saveEntityAsTemplate" type="primary" size="small">
                        <div class="inline-block">
                            <i class="fas fa-save"></i>
                        </div>
                        <div
                            class="inline-block ml-1 xl:inline-block xl:ml-1"
                            :class="{ hidden: entity.etype === 'File' }"
                        >
                            Save Entity as Template
                        </div>
                    </el-button>
                </div>
                <div>
                    <el-button @click="deleteEntity" type="danger" size="small">
                        <div class="inline-block">
                            <i class="fas fa-trash"></i>
                        </div>
                        <div
                            class="inline-block ml-1 xl:inline-block xl:ml-1"
                            :class="{ hidden: entity.etype === 'File' }"
                        >
                            Delete Entity
                        </div>
                    </el-button>
                </div>
            </div>
            <!-- /navbar: controls -->
        </div>
        <add-property-dialog-component
            v-if="definition && definition.inputs && definition.inputs.length"
            :visible="addPropertyDialogVisible"
            :inputs="definition.inputs"
            @close="addPropertyDialogVisible = false"
            @create:property="createProperty"
            @create-and-link:entity="createAndLinkEntity"
            @link:entity="linkEntity"
            @add:template="addTemplateAndLinkEntity"
        />
    </div>
</template>

<script>
import AddPropertyDialogComponent from "./AddPropertyDialog.component.vue";
import DataService from "./data.service.js";

export default {
    components: {
        AddPropertyDialogComponent,
    },
    props: {
        entity: {
            type: Object,
            required: true,
        },
        definition: {
            type: Object | undefined,
            required: true,
        },
    },
    data() {
        return {
            entityCount: 0,
            maxEntitiesPerTemplate: this.$store.state.configuration.maxEntitiesPerTemplate,
            loading: false,
            dataService: undefined,
            error: undefined,
            addPropertyDialogVisible: false,
            crateName: undefined,
        };
    },
    mounted() {
        this.dataService = new DataService({
            $http: this.$http,
            $log: this.$log,
        });
    },
    methods: {
        loadRootDataset() {
            this.$store.commit("setSelectedEntity", { id: "RootDataset" });
        },
        async showAddPropertyDialog() {
            this.addPropertyDialogVisible = true;
        },
        async createProperty({ property, value }) {
            await this.dataService.createProperty({
                srcEntityId: this.entity.id,
                property,
                value,
            });
            this.$emit("refresh");
        },
        async createAndLinkEntity({ property, etype, entityName }) {
            let { entity } = await this.dataService.createEntity({
                name: entityName,
                etype,
            });
            await this.linkEntity({ property, tgtEntityId: entity.id });
            this.$store.commit("setSelectedEntity", { id: entity.id });
        },
        async linkEntity({ property, tgtEntityId }) {
            await this.dataService.associate({
                srcEntityId: this.entity.id,
                property,
                tgtEntityId,
            });
            this.$emit("refresh");
        },
        async addTemplateAndLinkEntity({ property, templateId }) {
            let { entity } = await this.dataService.addTemplate({ templateId });
            await this.linkEntity({ property, tgtEntityId: entity.id });
        },
        async deleteEntity() {
            await this.dataService.deleteEntity({ id: this.entity.id });
            this.$store.commit("setSelectedEntity", { id: "RootDataset" });
        },
        async saveEntityAsTemplate() {
            await this.dataService.saveEntityAsTemplate({ id: this.entity.id });
        },
        async saveCrateAsTemplate() {
            await this.dataService.saveCrateAsTemplate({ name: this.crateName });
            this.crateName = undefined;
        },
        resolveFilePath(id) {
            let filePath = `${this.$store.state.target.folder.path}/${id}`;
            return filePath;
        },
    },
};
</script>

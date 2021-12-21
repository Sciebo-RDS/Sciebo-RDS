<template>
    <div class="flex flex-col space-y-2 divide-y divide-grey-200">
        <div
            v-for="(properties, name) of properties"
            :key="generateKey('forward', name)"
            class="flex flex-row pt-2"
            :class="{
                'bg-green-200 my-1 p-1 rounded': update.success === name,
                'bg-red-200 my-1 p-1 rounded': update.erro === name,
            }"
        >
            <div class="w-64">
                {{ name }}
            </div>
            <div class="w-full flex flex-col space-y-2">
                <div class="flex flex-row space-x-2">
                    <div v-if="help(name)">
                        <el-button @click="toggleHelp(name)" type="primary" size="mini">
                            <i class="fas fa-question-circle"></i>
                        </el-button>
                    </div>
                    <add-component
                        class="flex-grow"
                        v-if="inputs"
                        :property="name"
                        :definition="definition(name)"
                        :embedded="false"
                        @create:property="createProperty"
                        @create:entity="createEntityAndLink"
                        @link:entity="linkEntity"
                        @add:template="addTemplateAndLinkEntity"
                    />
                </div>
                <information-component type="info" align="left" v-if="showHelp === name">
                    {{ help(name) }}
                </information-component>
                <render-entity-property-component
                    v-for="property of properties"
                    :key="property.id"
                    :property="property"
                    @save:property="saveProperty"
                    @refresh="$emit('refresh')"
                />
            </div>
        </div>
    </div>
</template>

<script>
import RenderEntityPropertyComponent from "./RenderEntityProperty.component.vue";
import AddComponent from "./Add.component.vue";
import DataService from "./data.service.js";
import InformationComponent from "../Information.component.vue";

export default {
    components: {
        RenderEntityPropertyComponent,
        AddComponent,
        InformationComponent,
    },
    props: {
        entity: {
            type: Object,
            required: true,
        },
        properties: {
            type: Object,
            required: true,
        },
        inputs: {
            type: Array,
        },
    },
    data() {
        return {
            showHelp: false,
            update: {
                error: false,
                success: false,
            },
        };
    },
    watch: {
        properties: function() {
            this.loadTgtEntityData();
        },
    },
    mounted() {
        this.dataService = new DataService({
            $http: this.$http,
            $log: this.$log,
        });
        this.loadTgtEntityData();
    },
    methods: {
        generateKey(direction, name) {
            return `${direction}-${name}`;
        },
        definition(name) {
            return this.inputs ? this.inputs.filter((i) => i?.name === name)[0] : [];
        },
        help(name) {
            return this.definition(name)?.help;
        },
        toggleHelp(name) {
            this.showHelp = this.showHelp !== name ? name : false;
        },
        async loadTgtEntityData() {
            for (let property of Object.keys(this.properties)) {
                for (let [idx, entry] of this.properties[property].entries()) {
                    if (entry.tgtEntityId) {
                        let response = await this.$http.get({
                            route: `/entity/${entry.tgtEntityId}`,
                        });
                        if (response.status !== 200) {
                            //TODO handle error
                        }
                        let { entity } = await response.json();
                        this.properties[property][idx] = {
                            ...this.properties[property][idx],
                            tgtEntityName: entity.name,
                            tgtEntityType: entity.etype,
                            tgtEntityEid: entity.eid,
                        };
                        this.properties[property] = [...this.properties[property]];
                    }
                }
            }
        },
        async saveProperty(data) {
            try {
                await this.dataService.updateProperty(data);
                this.update.success = data.property;
                setTimeout(() => {
                    this.update.success = false;
                }, 1500);
            } catch (error) {
                this.update.error = data.property;
                setTimeout(() => {
                    this.update.error = false;
                }, 1500);
            }
        },
        async createProperty({ property, value }) {
            await this.dataService.createProperty({
                srcEntityId: this.entity.id,
                property,
                value,
            });
            this.$emit("refresh");
        },
        async createEntityAndLink({ property, entityName, etype }) {
            let { entity } = await this.dataService.createEntity({
                name: entityName,
                etype,
            });
            await this.dataService.associate({
                srcEntityId: this.entity.id,
                property,
                tgtEntityId: entity.id,
            });
            this.$store.commit("setSelectedEntity", { id: entity.id });
            // this.$emit("refresh");
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
            this.linkEntity({ property, tgtEntityId: entity.id });
        },
    },
};
</script>

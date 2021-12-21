<template>
    <div v-if="visible" class="flex flex-col m-4 p-2 border bg-indigo-100">
        <div class="flex flex-row">
            <div class="pt-2 mr-2">Add a property to this entity</div>
            <div class="flex-grow">
                <el-select
                    class="w-full"
                    v-model="property"
                    filterable
                    clearable
                    placeholder="Select a property to add"
                    @change="handlePropertySelection"
                >
                    <el-option
                        v-for="item in inputs"
                        :key="item.name"
                        :label="item.name"
                        :value="item.name"
                    >
                        <div class="flex flex-row">
                            <div class="w-64 text-gray-600">
                                {{ item.name }}
                            </div>
                            <div class="w-96 text-gray-500">
                                {{ item.help }}
                            </div>
                        </div>
                    </el-option>
                </el-select>
            </div>
            <div class="">
                <el-button @click="close"><i class="fas fa-times"></i></el-button>
            </div>
        </div>
        <div v-if="selectedProperty" class="flex flex-col">
            <div class="text-xs text-gray-600">
                {{ selectedProperty.help }}
            </div>
            <add-component
                class="mt-4"
                :property="property"
                :definition="selectedProperty"
                @create:property="createProperty"
                @create:entity="createAndLinkEntity"
                @link:entity="linkEntity"
                @add:template="addTemplate"
            />
        </div>
    </div>
</template>

<script>
import DataService from "./data.service.js";
import AddComponent from "./Add.component.vue";

export default {
    components: {
        AddComponent,
    },
    props: {
        inputs: {
            type: Array,
            required: true,
        },
        visible: {
            type: Boolean,
            required: true,
        },
    },
    data() {
        return {
            property: undefined,
            selectedProperty: undefined,
            addType: undefined,
        };
    },
    methods: {
        close() {
            this.property = undefined;
            this.selectedProperty = undefined;
            this.addType = undefined;
            this.$emit("close");
        },
        handlePropertySelection() {
            this.selectedProperty = undefined;
            this.$nextTick(() => {
                this.selectedProperty = this.inputs.filter((i) => i.name === this.property)[0];
            });
        },
        add({ type }) {
            this.addType = type;
        },
        createProperty(data) {
            this.$emit("create:property", data);
            this.close();
        },
        createAndLinkEntity(data) {
            this.$emit("create-and-link:entity", data);
            this.close();
        },
        linkEntity(data) {
            this.$emit("link:entity", data);
            this.close();
        },
        addTemplate(data) {
            this.$emit("add:template", data);
            this.close();
        },
    },
};
</script>

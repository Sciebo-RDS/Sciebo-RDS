<template>
    <div class="flex flex-col">
        <add-control-component
            :types="definition['type']"
            :embedded="embedded"
            v-if="definition && !addType"
            @add="add"
        />

        <div v-if="addType" class="" :class="{ 'bg-indigo-100 p-2': !embedded }">
            <div class="flex flex-row">
                <!-- <div><i class="text-xl fas fa-link"></i> Associate an entity</div> -->
                <div class="flex-grow"></div>
                <div v-if="!embedded">
                    <el-button @click="close" size="mini">
                        <i class="fas fa-times fa-fw"></i>
                    </el-button>
                </div>
            </div>
            <div v-if="addSimpleType" class="">
                <text-component
                    v-if="addType === 'Text'"
                    :property="property"
                    :auto-save="false"
                    @save:property="createProperty"
                />
                <date-component
                    v-if="addType === 'Date'"
                    :property="property"
                    @save:property="createProperty"
                />
                <date-time-component
                    v-if="addType === 'DateTime'"
                    :property="property"
                    @save:property="createProperty"
                />
                <number-component
                    v-if="['Number', 'Float', 'Integer'].includes(addType)"
                    :property="property"
                    @save:property="createProperty"
                />
                <time-component
                    v-if="addType === 'Time'"
                    :property="property"
                    @save:property="createProperty"
                />
            </div>
            <div v-else class="">
                <div class="flex flex-col space-y-2 divide-y divide-gray-300 text-gray-600 ">
                    <div class="w-full flex flex-col justify-center">
                        <div class="flex flex-row">
                            <div class="mr-2 text-sm pt-1">
                                Create and associate a new:
                            </div>
                            <div>
                                <el-button
                                    @click="createEntityAndLink"
                                    type="success"
                                    size="mini"
                                    class="focus:outline-none focus:border-2 focus:border-green-600"
                                >
                                    <i class="fas fa-plus"></i>&nbsp;{{ addType }}
                                </el-button>
                            </div>
                        </div>
                    </div>
                    <div class="w-full py-2">
                        <div class="text-sm">
                            OR - Associate an existing '{{ addType }}': lookup by @id, @type, or
                            name
                        </div>
                        <autocomplete-component
                            :type="addType"
                            by="name"
                            @link:entity="linkEntity"
                            @add:template="addTemplate"
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AddControlComponent from "./AddControl.component.vue";
import TextComponent from "./Text.component.vue";
import DateComponent from "./Date.component.vue";
import DateTimeComponent from "./DateTime.component.vue";
import TimeComponent from "./Time.component.vue";
import NumberComponent from "./Number.component.vue";
import DataService from "./data.service.js";
import AutocompleteComponent from "./AutoComplete.component.vue";

export default {
    components: {
        AddControlComponent,
        TextComponent,
        DateComponent,
        DateTimeComponent,
        TimeComponent,
        NumberComponent,
        AutocompleteComponent,
    },
    props: {
        embedded: {
            type: Boolean,
            default: true,
        },
        property: {
            type: String,
            required: true,
        },
        definition: {
            type: Object | undefined,
            required: true,
        },
    },
    data() {
        return {
            simpleTypes: ["Text", "Date", "DateTime", "Time", "Number", "Float", "Integer"],
            addType: undefined,
        };
    },
    computed: {
        addSimpleType() {
            return this.simpleTypes.includes(this.addType);
        },
    },
    mounted() {
        this.dataService = new DataService({
            $http: this.$http,
            $log: this.$log,
        });
    },
    methods: {
        close() {
            this.addType = undefined;
        },
        add({ type }) {
            this.addType = type;
        },
        createProperty(data) {
            this.$emit("create:property", data);
        },
        createEntityAndLink() {
            this.$emit("create:entity", {
                etype: this.addType,
                property: this.property,
                entityName: "new entity",
            });
        },
        linkEntity({ entity }) {
            this.$emit("link:entity", {
                property: this.property,
                tgtEntityId: entity.id,
            });
        },
        addTemplate({ template }) {
            this.$emit("add:template", {
                property: this.property,
                templateId: template.id,
            });
        },
    },
};
</script>

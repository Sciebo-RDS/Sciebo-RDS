<template>
    <div class="flex flex-col space-y-1 border-b pb-2">
        <!-- entity id -->
        <div
            class="flex flex-row"
            :class="{
                'bg-green-200 p-1 rounded': update.success === 'eid',
                'bg-red-200 p-1 rounded': update.error === 'eid',
            }"
            v-if="entity.eid !== './'"
        >
            <div class="w-64 pt-1">
                @id
            </div>
            <entity-id-component
                class="w-full"
                :value.sync="entity.eid"
                @save:property="saveEntityProperty"
                v-if="!['Dataset', 'File'].includes(entity.etype)"
            />
            <div
                v-if="['Dataset', 'File'].includes(entity.etype)"
                class="w-full"
            >
                {{ entity.eid }}
            </div>
        </div>

        <!-- entity type -->
        <div class="flex flex-row" v-if="entity.eid !== './'">
            <div class="w-64 pt-1">@type</div>
            <div class="w-full">{{ entity.etype }}</div>
        </div>

        <!-- entity name -->
        <div
            class="flex flex-row"
            :class="{
                'bg-green-200 p-1 rounded': update.success === 'name',
                'bg-red-200 p-1 rounded': update.error === 'name',
            }"
        >
            <div class="w-64">name</div>

            <text-component
                class="w-full"
                type="text"
                property="name"
                :value.sync="entity.name"
                @save:property="saveEntityProperty"
            />
        </div>
    </div>
</template>

<script>
import EntityIdComponent from "./EntityId.component.vue";
import TextComponent from "./Text.component.vue";
import DataService from "./data.service.js";

export default {
    components: {
        EntityIdComponent,
        TextComponent,
    },
    props: {
        entity: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            dataService: undefined,
            update: {
                error: false,
                success: false,
            },
        };
    },
    mounted() {
        this.dataService = new DataService({
            $http: this.$http,
            $log: this.$log,
        });
    },
    methods: {
        async saveEntityProperty(data) {
            try {
                await this.dataService.updateEntityProperty({
                    id: this.entity.id,
                    property: data.property,
                    value: data.value,
                });
                this.update.success = data.property;
                setTimeout(() => {
                    this.update.success = false;
                }, 1500);
            } catch (error) {
                this.update.error = data.property;
                setTimeout(() => {
                    this.update.error = false;
                    this.getEntity();
                }, 1500);
            }
        },
    },
};
</script>

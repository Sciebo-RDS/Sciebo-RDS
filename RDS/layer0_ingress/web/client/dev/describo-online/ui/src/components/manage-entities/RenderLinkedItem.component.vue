<template>
    <div class="flex flex-row">
        <div class="flex flex-col bg-yellow-200 p-3 cursor-pointer rounded-l" @click="loadEntity">
            <div class="text-sm flex flex-row space-x-1">
                <type-icon-component
                    class="mr-2 text-gray-700"
                    :type="entity.tgtEntityType"
                    v-if="entity.tgtEntityType"
                />
                <div>{{ entity.tgtEntityType }}:</div>
                <span v-if="entity.tgtEntityName">{{ entity.tgtEntityName }}</span>
                <span v-else>{{ entity.tgtEntityEid }}</span>
            </div>
        </div>
        <delete-property-component
            class="bg-yellow-200 cursor-pointer rounded-r pl-4 pt-2 pr-1"
            :property="entity"
            @refresh="$emit('refresh')"
        />
    </div>
</template>

<script>
import TypeIconComponent from "./TypeIcon.component.vue";
import DeletePropertyComponent from "./DeleteProperty.component.vue";

export default {
    components: {
        TypeIconComponent,
        DeletePropertyComponent,
    },
    props: {
        entity: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {};
    },
    methods: {
        loadEntity() {
            this.$store.commit("setSelectedEntity", {
                id: this.entity.tgtEntityId,
            });
        },
    },
};
</script>

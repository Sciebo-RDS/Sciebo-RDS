<template>
    <div class="flex flex-col space-y-1">
        <div class="mt-4 text-lg" v-if="hasReverseProperties">
            This entity is referenced by:
        </div>
        <div
            v-for="(properties, name) of properties"
            :key="generateKey('reverse', name)"
            class="flex flex-row"
        >
            <div class="flex flex-col space-y-2">
                <render-reverse-item-link-component
                    v-for="property of properties"
                    :key="property.id"
                    :entity="property"
                />
            </div>
        </div>
    </div>
</template>

<script>
import RenderReverseItemLinkComponent from "./RenderReverseItemLink.component.vue";

export default {
    components: {
        RenderReverseItemLinkComponent,
    },
    props: {
        properties: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {};
    },
    computed: {
        hasReverseProperties: function() {
            return Object.keys(this.properties).length;
        },
    },
    mounted() {
        this.loadTgtEntityData();
    },
    methods: {
        generateKey(direction, name) {
            return `${direction}-${name}`;
        },
        async loadTgtEntityData() {
            for (let property of Object.keys(this.properties)) {
                for (let [idx, entry] of this.properties[property].entries()) {
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
                    };
                    this.properties[property] = [...this.properties[property]];
                }
            }
        },
    },
};
</script>

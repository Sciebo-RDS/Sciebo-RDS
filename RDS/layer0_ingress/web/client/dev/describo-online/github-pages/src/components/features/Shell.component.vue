<template>
    <div class="flex flex-col space-y-4 md:space-y-10 my-10">
        <div class="text-xl lg:text-4xl text-center">
            Features
            <span class="inline-block text-lg">(click on an image to expand)</span>
        </div>
        <div v-for="(item, idx) of items" :key="idx">
            <render-feature-component :item="item" />
        </div>
    </div>
</template>

<script>
import RenderFeatureComponent from "./RenderFeature.component.vue";

export default {
    components: {
        RenderFeatureComponent,
    },
    data() {
        return {
            expandImage: false,
            items: [
                {
                    image: "images/manage-entities.png",
                    text: "Manage the entities you create to describe your data.",
                },
                {
                    image: "images/manage-templates.png",
                    text: "Save entity and full crate templates for reuse.",
                },
                {
                    image: "images/person.png",
                    text: "Create entities and attach them to other entities.",
                },
                {
                    image: "images/date.png",
                    text: "Link specific entity types to properties.",
                },
                {
                    image: "images/describe-files-with-preview.png",
                    text: "Describe files. See previews of known formats.",
                },
                {
                    image: "images/referenced-by.png",
                    text: "See where entities are referenced.",
                },
            ],
        };
    },
};
</script>

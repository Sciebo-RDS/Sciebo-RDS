<template>
    <div class="mb-10">
        <header-component class="mt-4" />
        <features-link-component class="block md:hidden" />
        <header-images-component />
        <features-link-component class="hidden md:block" />
        <about-component class="mt-6" />
    </div>
</template>

<script>
import HeaderComponent from "./Header.component.vue";
import HeaderImagesComponent from "./HeaderImages.component.vue";
import AboutComponent from "./About.component.vue";
import FeaturesLinkComponent from "./FeaturesLink.component.vue";
export default {
    components: {
        HeaderComponent,
        HeaderImagesComponent,
        AboutComponent,
        FeaturesLinkComponent,
    },
    data() {
        return {};
    },
};
</script>

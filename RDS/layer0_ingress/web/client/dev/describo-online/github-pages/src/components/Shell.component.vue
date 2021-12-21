<template>
    <div class="mb-10">
        <navigation-component class="mt-6" />
        <router-view />
        <footer-component class="mt-6" />
    </div>
</template>

<script>
import NavigationComponent from "./Navigation.component.vue";
import FooterComponent from "./Footer.component.vue";
export default {
    components: {
        NavigationComponent,
        FooterComponent,
    },
    data() {
        return {};
    },
};
</script>

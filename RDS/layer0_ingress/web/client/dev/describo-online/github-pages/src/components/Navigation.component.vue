<template>
    <div class="flex flex-row space-x-4 md:space-x-8 border-b-2 pb-2">
        <div class="flex-grow"></div>
        <div class="hover:text-orange-600" :class="{ 'text-orange-600': activeRoute === 'home' }">
            <router-link to="/"><i class="fas fa-home"></i></router-link>
        </div>
        <div
            class="hover:text-orange-600"
            :class="{ 'text-orange-600': activeRoute === 'features' }"
        >
            <router-link to="features">features</router-link>
        </div>
        <div class="hidden md:block">
            <router-link to="about">about</router-link>
        </div>
        <div>
            <a
                href="https://github.com/Arkisto-Platform/describo-online"
                target="_blank"
                class="hover:text-orange-600"
                ><i class="fab fa-github"></i> github</a
            >
        </div>
        <div class="hidden md:block">
            <a
                href="https://github.com/Arkisto-Platform/describo-online/issues"
                target="_blank"
                class="hover:text-orange-600"
                >issues</a
            >
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {};
    },
    computed: {
        activeRoute: function() {
            return this.$route.name;
        },
    },
};
</script>

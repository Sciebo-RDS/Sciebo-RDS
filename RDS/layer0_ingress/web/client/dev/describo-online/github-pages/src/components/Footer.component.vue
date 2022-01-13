<template>
    <div class="flex flex-row space-y-1 border-t-2 justify-around">
        <div class="hidden md:block flex-grow"></div>
        <div class="flex flex-row space-x-8">
            <div class="flex flex-col md:flex-row md:space-x-8">
                <div class="hover:text-orange-600">
                    <router-link to="features">features</router-link>
                </div>
                <!-- <div>
                    <a
                        href="https://github.com/Arkisto-Platform/describo-online/wiki"
                        class="hover:text-orange-600"
                        >docs</a
                    >
                </div> -->
                <div class="hover:text-orange-600">
                    <router-link to="about">about</router-link>
                </div>
            </div>
            <div class="flex flex-col md:flex-row md:space-x-8">
                <div>
                    <a
                        href="https://github.com/Arkisto-Platform/describo-online"
                        class="hover:text-orange-600"
                        ><i class="fab fa-github"></i> github</a
                    >
                </div>
                <div>
                    <a
                        href="https://github.com/Arkisto-Platform/describo-online/issues"
                        class="hover:text-orange-600"
                        >issues</a
                    >
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {};
    },
};
</script>

<template>
    <div class="flex flex-row space-x-4 p-2 bg-indigo-100 py-4 px-10 text-xl text-gray-800">
        <div
            @click="navTo('/')"
            class="cursor-pointer"
            :class="{ 'text-blue-500': currentRoute === 'root' }"
        >
            <i class="fas fa-home"></i>
        </div>
        <div>{{ siteName }}</div>
        <div
            @click="navTo({ path: '/templates' })"
            class="text-base pt-1 cursor-pointer"
            :class="{ 'text-blue-500': currentRoute === 'templates' }"
        >
            <i class="fas fa-list"></i>
            Manage My Templates
        </div>
        <div class="flex flex-grow"></div>
        <div
            @click="navTo({ name: 'logout' })"
            class="text-base pt-1 cursor-pointer"
            v-if="!embeddedSession"
        >
            <i class="fas fa-sign-out-alt"></i>
        </div>
    </div>
</template>

<script>
import HTTPService from "@/components/http.service";

export default {
    data() {
        return {
            siteName: this.$store.state.configuration.siteName,
            embeddedSession: false,
        };
    },
    computed: {
        currentRoute: function() {
            return this.$route.name;
        },
    },
    mounted() {
        this.setMode();
    },
    methods: {
        navTo(path) {
            this.$router.push(path).catch((err) => {});
        },
        async setMode() {
            let httpService = new HTTPService({ $auth: this.$auth });
            let response = await httpService.get({ route: "/session" });
            if (response.status !== 200) {
                // do nothing
            }
            let { session, embeddedSession } = await response.json();
            this.embeddedSession = embeddedSession;
        },
    },
};
</script>

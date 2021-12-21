<template>
    <div v-if="error" class="text-lg rounded m-8 bg-red-400 text-center p-4">
        There was an issue getting a token from owncloud. The service is unavailable at this time.
    </div>
</template>

<script>
export default {
    data() {
        return {
            error: false,
        };
    },
    mounted() {
        this.getToken();
    },
    methods: {
        async getToken() {
            let code = this.$route.query.code;
            this.$router.push(this.$route.path);

            try {
                await this.owncloudAuthenticationManager.getOauthToken({
                    code,
                });
                this.$store.commit("setTargetResource", {
                    resource: "owncloud",
                });
            } catch (error) {
                this.error = true;
                await new Promise((resolve) => setTimeout(resolve, 5000));
            }
            this.$router.push("/");
        },
    },
};
</script>

<template>
    <div class="flex flex-col justify-center h-screen">
        <div class="flex flex-col text-center p-20 m-64">
            <div>setting up your session</div>
            <div>
                <el-progress
                    class="my-2"
                    :stroke-width="10"
                    :show-text="false"
                    :percentage="percentage"
                ></el-progress>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            percentage: 0,
        };
    },
    async beforeMount() {
        this.percentage = 50;

        await this.$oktaAuth.storeTokensFromRedirect();
        const user = await this.$oktaAuth.getUser();
        await this.$http.post({
            route: "/session/okta",
            body: {
                name: user.name,
                email: user.email,
            },
        });
        this.percentage = 100;
        await new Promise((resolve) => setTimeout(resolve, 500));
        this.$router.replace({
            path: "/",
        });
    },
};
</script>

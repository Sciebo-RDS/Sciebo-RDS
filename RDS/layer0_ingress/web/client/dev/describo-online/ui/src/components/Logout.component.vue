<template>
    <div class="w-full h-full flex flex-row justify-center items-center">
        <div class="">logging you out... one moment</div>
    </div>
</template>

<script>
import { removeSessionSID } from "@/components/auth.service";

export default {
    data() {
        return {};
    },
    mounted() {
        this.logout();
    },
    methods: {
        async logout() {
            window.localStorage.removeItem("vuex");
            removeSessionSID();
            try {
                if (this.$oktaAuth) {
                    await this.$oktaAuth.signOut({
                        postLogoutRedirectUri: `${window.location.origin}/login`,
                    });
                } else {
                    this.$router.push("/login");
                }
            } catch (error) {
                this.$router.push("/login");
            }
        },
    },
};
</script>

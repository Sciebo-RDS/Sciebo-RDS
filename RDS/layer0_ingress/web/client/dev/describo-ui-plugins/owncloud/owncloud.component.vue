<template>
    <div class="flex flex-col space-y-2">
        <div>
            <el-button type="primary" @click.prevent="getCurrentSession" :disabled="loggingIn">
                login to ownCloud
            </el-button>
        </div>
        <div v-if="showOwncloudInputForm" class="flex flex-row space-x-2 p-4 border rounded">
            <div>
                <el-button
                    @click.prevent="
                        loggingIn = false;
                        showOwncloudInputForm = false;
                    "
                >
                    <i class="fas fa-times"></i>
                </el-button>
            </div>
            <div class="flex-grow">
                <el-select
                    v-model="selectedOwncloudServer"
                    placeholder="Select a server to use"
                    class="w-full"
                >
                    <el-option
                        v-for="server in owncloudServers"
                        :key="server.url"
                        :label="server.name"
                        :value="server"
                        :value-key="server.url"
                    >
                        <div>{{ server.name }} ({{ server.url }})</div>
                    </el-option>
                </el-select>
            </div>
            <div>
                <el-button @click.prevent="login">
                    <i class="fas fa-arrow-right"></i>
                </el-button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            showOwncloudInputForm: false,
            owncloudServers: [],
            selectedOwncloudServer: undefined,
            loggingIn: false,
        };
    },
    methods: {
        async getCurrentSession() {
            this.loggingIn = true;

            let { configuration } = await this.owncloudAuthenticationManager.getConfiguration();
            this.owncloudServers = configuration;
            if (this.owncloudServers.length === 1) {
                this.selectedOwncloudServer = this.owncloudServers[0];
                this.login();
            } else {
                this.showOwncloudInputForm = true;
            }
        },
        async login() {
            await this.owncloudAuthenticationManager.getOauthCode({
                server: this.selectedOwncloudServer,
            });
        },
    },
};
</script>

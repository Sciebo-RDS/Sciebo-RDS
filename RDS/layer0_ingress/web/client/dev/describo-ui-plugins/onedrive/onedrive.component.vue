<template>
    <div class="flex flex-row">
        <div>
            <el-button type="primary" @click.prevent="login" :disabled="loggedIn || loggingIn">
                login to Microsoft OneDrive
            </el-button>
        </div>
        <div v-if="loggingIn" class="flex-grow">
            <el-select
                v-if="drives && drives.length"
                class="w-full"
                v-model="selectedDrive"
                placeholder="Select the OneDrive to work with"
                @change="saveConfiguration"
            >
                <el-option
                    v-for="drive of drives"
                    :key="drive.id"
                    :label="drive.webUrl"
                    :value="drive.id"
                >
                </el-option>
            </el-select>
        </div>
    </div>
</template>

<script>
import HTTPService from "@/components/http.service";

export default {
    data() {
        return {
            loggingIn: false,
            loggedIn: false,
            account: undefined,
            token: undefined,
            drives: undefined,
            selectedDrive: undefined,
        };
    },
    methods: {
        async login() {
            this.loggingIn = true;
            this.loggedIn = false;
            await this.onedriveAuthenticationManager.login();
            let { drives } = await this.onedriveAuthenticationManager.loadDrives();
            this.drives = drives;
            if (drives.length === 1) this.selectedDrive = drives[0].id;
            if (this.selectedDrive) {
                this.saveConfiguration();
            }
        },
        async logout() {
            this.onedriveAuthenticationManager.logout();
        },
        async saveConfiguration() {
            const drive = this.drives.filter((d) => d.id === this.selectedDrive)[0];
            let token = this.onedriveAuthenticationManager.getToken();
            let configuration = {
                service: "onedrive",
                token: {
                    access_token: token.accessToken,
                    expires: token.expiresOn,
                },
                account: token.account,
                scopes: token.scopes,
                drive_id: drive.id,
                drive_type: drive.driveType,
            };
            await this.onedriveAuthenticationManager.save({ configuration });
            this.loggingIn = false;
            this.loggedIn = true;
            this.$store.commit("setTargetResource", {
                resource: "onedrive",
            });
        },
    },
};
</script>

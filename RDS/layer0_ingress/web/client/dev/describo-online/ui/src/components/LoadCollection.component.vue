<template>
    <el-card class="box-card" v-if="msg">
        <div class="flex flex-row">
            <!-- <div>
                <el-button @click="loadFolder" :disabled="loading">
                    load folder
                </el-button>
            </div> -->
            <div class="ml-2 pt-2">{{ msg }}</div>
        </div>
    </el-card>
</template>

<script>
import { round } from "lodash";

export default {
    data() {
        return {
            loading: false,
            msg: undefined,
        };
    },
    computed: {
        target() {
            return this.$store.state.target;
        },
    },
    mounted() {
        this.$socket.on("loadRouteHandler", (response) => {
            this.msg = `${response.msg}`;
        });
        if (!this.$store.state.collection.id) {
            this.loadFolder();
        }
    },
    methods: {
        async loadFolder() {
            this.loading = true;
            let response = await this.$http.post({
                route: "/load",
                body: {
                    resource: this.target.resource,
                    folder: this.target.folder.path,
                    id: this.target.folder.id,
                },
            });
            if (response.status !== 200) {
                this.$store.commit("setTargetResource", {
                    resource: undefined,
                    folder: undefined,
                });
                this.$store.commit("setActiveCollection", {});
                this.$store.commit("setSelectedEntity", { id: "RootDataset" });
                return;
            }
            let { collection } = await response.json();
            this.$store.commit("setActiveCollection", collection);
            this.loading = false;
            await new Promise((resolve) => setTimeout(resolve, 1000));
            this.msg = undefined;
        },
    },
};
</script>

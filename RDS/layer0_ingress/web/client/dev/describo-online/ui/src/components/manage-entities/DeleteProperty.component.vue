<template>
    <div class="">
        <el-button @click="deleteProperty" type="danger" size="mini">
            <div v-show="type === 'unlink'" class="inline-block">
                <i class="fas fa-unlink"></i>
            </div>
            <div v-show="type === 'delete'" class="inline-block">
                <i class="fas fa-trash"></i>
            </div>
        </el-button>
    </div>
</template>

<script>
import DataService from "./data.service.js";

export default {
    props: {
        type: {
            type: String,
            default: "unlink",
            validator: (val) => {
                return ["delete", "unlink"].includes(val);
            },
        },
        property: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {};
    },
    mounted() {
        this.dataService = new DataService({
            $http: this.$http,
            $log: this.$log,
        });
    },
    methods: {
        async deleteProperty() {
            await this.dataService.deleteProperty({
                entityId: this.property.entityId,
                propertyId: this.property.id,
            });
            this.$emit("refresh");
        },
    },
};
</script>

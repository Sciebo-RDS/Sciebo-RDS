<template>
    <div class="flex flex-row">
        <el-date-picker
            v-model="internalValue"
            type="datetime"
            placeholder="Pick a date and time"
            @change="save"
            :clearable="false"
        >
        </el-date-picker>
    </div>
</template>

<script>
import { startOfDay } from "date-fns";

export default {
    props: {
        property: {
            type: String,
            required: true,
        },
        value: {
            type: String,
        },
    },
    data() {
        return {
            internalValue: this.value,
        };
    },
    watch: {
        value: function() {
            this.internalValue = this.value;
        },
    },
    methods: {
        save() {
            this.$emit("save:property", {
                property: this.property,
                value: this.internalValue.toISOString(),
            });
        },
    },
    save() {},
};
</script>

<style lang="scss" scoped>
.style-text-input {
    width: 500px;
}
</style>

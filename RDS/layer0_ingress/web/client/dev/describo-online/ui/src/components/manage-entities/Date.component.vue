<template>
    <div class="flex flex-row">
        <el-date-picker
            v-model="internalValue"
            type="date"
            placeholder="Pick a date"
            format="MMMM d, yyyy"
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
                value: startOfDay(this.internalValue).toISOString(),
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

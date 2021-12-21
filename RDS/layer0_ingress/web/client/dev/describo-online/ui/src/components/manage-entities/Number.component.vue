<template>
    <div class="flex flex-row flex-grow space-x-2">
        <div class="flex-grow">
            <el-input
                class="w-full"
                type="number"
                @input="debouncedSave"
                v-model="internalValue"
                resize="vertical"
            ></el-input>
        </div>
    </div>
</template>

<script>
import { debounce } from "lodash";

export default {
    props: {
        property: {
            type: String,
            required: true,
        },
        value: {
            type: String,
        },
        autoSave: {
            type: Boolean,
            default: true,
        },
    },
    data() {
        return {
            internalValue: this.value,
            debouncedSave: this.autoSave ? debounce(this.save, 1000) : () => {},
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
                value: this.internalValue,
            });
        },
    },
};
</script>

<style lang="scss">
.el-input-number {
    min-width: 300px;
}
</style>

<template>
    <div class="flex flex-row flex-grow space-x-2">
        <div class="flex-grow">
            <el-input
                class="w-full"
                :type="type"
                @input="debouncedSave"
                v-model="internalValue"
                resize="vertical"
            ></el-input>
        </div>
        <div v-if="!autoSave">
            <el-button @click="save" type="success" size="mini">
                <i class="fas fa-check fa-fw"></i>
            </el-button>
        </div>
    </div>
</template>

<script>
import { debounce } from "lodash";

export default {
    props: {
        type: {
            type: String,
            default: "textarea",
            validator: (val) => {
                return ["text", "textarea"].includes(val);
            },
        },
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

<style lang="scss" scoped></style>

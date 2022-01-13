<template>
    <div>
        <div class="flex flex-row flex-wrap space-x-1" v-if="allowedTypes.length < 5">
            <div v-for="(type, idx) of allowedTypes" :key="idx">
                <el-button
                    @click="add(type)"
                    type="success"
                    size="mini"
                    class="focus:outline-none focus:border-2 focus:border-green-600"
                >
                    <i class="fas fa-plus"></i>&nbsp;{{ type }}
                </el-button>
            </div>
        </div>
        <div v-else>
            <el-select
                v-model="selectedType"
                placeholder="Select a type to add"
                @change="add"
                clearable
                size="small"
                class="w-full"
            >
                <el-option
                    v-for="(type, idx) in allowedTypes"
                    :key="idx"
                    :label="type"
                    :value="type"
                >
                </el-option>
            </el-select>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        embedded: {
            type: Boolean,
            default: false,
            validator: (val) => [true, false].includes(val),
        },
        types: {
            type: Array,
            required: true,
        },
    },
    data() {
        return {
            selectedType: undefined,
            allowedTypes: [],
            typeExclusions: [],
            // typeExclusions: ["File", "Dataset"],
        };
    },
    watch: {
        types: function() {
            this.init();
        },
    },
    mounted() {
        this.init();
        if (this.embedded && this.types.length === 1) this.add(this.types[0]);
    },
    methods: {
        init() {
            this.allowedTypes = this.types.filter((type) => !this.typeExclusions.includes(type));
        },
        add(type) {
            this.selectedType = type;
            this.$emit("add", { type });
        },
    },
};
</script>

<style lang="scss" scoped></style>

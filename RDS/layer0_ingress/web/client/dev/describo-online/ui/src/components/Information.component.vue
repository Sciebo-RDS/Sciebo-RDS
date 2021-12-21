<template>
    <div
        class="flex flex-row text-gray-800 p-4 rounded"
        :class="{
            'justify-left': align === 'left',
            'justify-center': align === 'center',
            'justify-right': align === 'right',
            'bg-gray-200': type === 'info',
            'bg-green-200': type === 'success',
            'bg-yellow-200': type === 'warning',
            'bg-red-200': type === 'danger',
        }"
    >
        <div class="text-blue-600 text-3xl" v-show="type === 'info'">
            <i class="fas fa-info-circle"></i>
        </div>
        <div class="text-green-600 text-3xl" v-show="type === 'success'">
            <i class="far fa-check-circle"></i>
        </div>
        <div class="text-yellow-600 text-3xl" v-show="type === 'warning'">
            <i class="fas fa-exclamation-triangle"></i>
        </div>
        <div class="text-red-600 text-3xl" v-show="type === 'danger'">
            <i class="fas fa-radiation-alt"></i>
        </div>
        <div class="ml-2 pt-1">
            <slot></slot>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        align: {
            type: String,
            default: "center",
            validator: (val) => {
                return ["left", "center", "right"].includes(val);
            },
        },
        type: {
            type: String,
            required: true,
            validator: (val) => {
                return ["info", "success", "warning", "danger"].includes(val);
            },
        },
    },
    data() {
        return {};
    },
};
</script>

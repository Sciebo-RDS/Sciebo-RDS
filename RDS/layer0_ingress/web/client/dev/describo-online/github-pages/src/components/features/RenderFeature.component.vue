<template>
    <div
        class="flex flex-col md:flex-row p-8 bg-blue-100 border-2 border-gray-400 justify-center"
    >
        <div
            class="border border-gray-400 p-1 flex flex-row justify-center"
            :class="{
                'w-full md:w-1/2': !expandImage,
            }"
            @click="expandImage = !expandImage"
        >
            <img :src="item.image" class="object-contain" />
        </div>
        <div
            v-if="!expandImage"
            class="text-sm md:text-xl w-full md:w-1/2 p-4"
            v-html="item.text"
        ></div>
    </div>
</template>

<script>
export default {
    props: {
        item: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            expandImage: false,
        };
    },
};
</script>

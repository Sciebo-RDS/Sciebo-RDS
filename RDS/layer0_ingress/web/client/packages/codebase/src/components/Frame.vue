<template>
  <div
    class="ma-0 pa-0 fill-height fullsize"
    style="height: 100%; width: 100%; border: 0px"
  >
    <iframe
      :src="source"
      class="ma-0 pa-0 fullsize"
      style="
        position: absolute;
        top: 0px;
        height: 100%;
        width: 100%;
        border: 0px;
        overflow-x: hidden;
      "
    />

    <v-card
      class="text-center pa-2"
      id="getting-started-button"
      style="width: 100%; position: absolute; bottom: 0px"
      tile
      flat
      v-if="!!$slots.default"
    >
      <slot></slot>
    </v-card>
  </div>
</template>

<script>
export default {
  props: {
    source: String,
  },
};
</script>

<style scoped>
iframe {
  position: absolute;
  top: 0px;
  height: 100%;
  width: 100%;
  border: none;
  overflow-x: hidden;
}

.fullsize {
  height: 100%;
  width: 100%;
  border: 0px;
}
</style>

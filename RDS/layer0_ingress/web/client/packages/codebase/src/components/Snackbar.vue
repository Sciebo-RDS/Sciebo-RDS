<template>
  <v-snackbar v-model="snackbar" variant="tonal" color="primary" :multi-line="multiLine" :timeout="timeout">
    {{ message }}

    <template v-slot:action="{ attrs }">
      <v-btn color="primary" text v-bind="attrs" @click="hide()">
        <translate>Close</translate>
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  data() {
    return {
      message: "Hey there, i am the snackbar.",
      snackbar: false,
      multiLine: true,
      timeout: -1,
    };
  },
  methods: {
    show() {
      this.snackbar = true;
    },
    hide() {
      this.snackbar = false;
    },
    toggle() {
      this.snackbar = !this.snackbar;
    },
  },
  beforeMount() {
    this.$root.$on("showsnackbar", (message) => {
      this.message = message;
      this.show();
    });
    this.$root.$on("hidesnackbar", () => {
      this.hide();
    });
  },
};
</script>

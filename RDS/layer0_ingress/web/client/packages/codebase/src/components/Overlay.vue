<template>
  <div class="text-center">
    <v-overlay :value="visible">
      <v-container flex>
        <v-row align="center" justify="center">
          <v-col>
            <v-progress-circular indeterminate size="64">
              <translate>Wait</translate>
            </v-progress-circular>
          </v-col>
        </v-row>
        <v-row align="center" justify="center">
          <v-col>{{ text }}</v-col>
        </v-row>
      </v-container>
    </v-overlay>
  </div>
</template>

<script>
export default {
  data: () => ({
    visible: true,
  }),
  computed: {
    text() {
      if (this.subtext === undefined) {
        return this.$gettext("Service activation in progress");
      }
      return this.subtext;
    },
  },
  props: {
    subtext: {
      type: String,
      default: undefined,
    },
  },
  beforeCreate() {
    this.$root.$on("showoverlay", () => {
      this.show();
    });

    this.$root.$on("hideoverlay", () => {
      this.hide();
    });
  },
  methods: {
    triggerOverlay() {
      this.visible = !this.visible;
    },
    hide() {
      this.visible = false;
    },
    show() {
      this.visible = true;
    },
  },
};
</script>

<template>
  <v-container fluid>
    <v-btn depressed @click="uninstallRDS" color="error">
      <translate>Uninstall sciebo RDS</translate>
    </v-btn>
  </v-container>
</template>

<script>
export default {
  name: "RevokeButton",
  computed: {
    ...mapGetters({
      ownCloudServicename: "getOwnCloudServername",
    }),
  },
  methods: {
    uninstallRDS() {
      this.$store.dispatch(
        "removeService",
        this.getInformations("port-owncloud-" + this.ownCloudServicename)
      );
    },
  },
};
</script>

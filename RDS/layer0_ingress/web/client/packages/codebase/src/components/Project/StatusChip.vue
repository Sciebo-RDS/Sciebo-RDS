<template>
  <v-card flat color="transparent">
    <v-chip v-if="this.status == 0"
      color="warning"
      class="caption"
      outlined
      label
      small>
      unnamed
    </v-chip>
    <v-chip v-if="this.status >= 1 && this.status <= 2"
      color="info"
      class="caption"
      outlined
      label
      small>
      draft
    </v-chip>
    <v-chip
      v-else-if="this.status == 3"
      color="success"
      class="caption"
      outlined
      label
      small
      >published
      <v-icon
        class="ml-1">
        mdi-lock
      </v-icon>
    </v-chip>
    <v-chip
      v-else-if="this.status == 4"
      color="error"
      outlined
      small
      label
      class="caption"
      >archived
      <v-icon
        class="ml-1">
        mdi-lock
      </v-icon>
    </v-chip>
  </v-card>
</template>

<script>
export default {
  props: ["status"],
};
</script>

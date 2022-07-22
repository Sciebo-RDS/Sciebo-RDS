<template>
  <v-card flat color="transparent">
    <v-chip v-if="this.status <= 2"
      color="light-green lighten-1"
      small>
      <translate>draft</translate>
    </v-chip>
    <v-chip
      v-else-if="this.status == 3"
      color="lighten-1"
      small
      ><translate>published</translate>
      <v-icon
      class="ml-1">
        mdi-lock
      </v-icon>
    </v-chip>
    <v-chip
      v-else-if="this.status == 4"
      color="red lighten-3"
      small
      ><translate>archived</translate>
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

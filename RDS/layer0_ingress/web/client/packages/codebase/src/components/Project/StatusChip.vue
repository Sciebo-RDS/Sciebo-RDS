<template>
  <v-card flat color="transparent">
    <v-chip v-if="this.status == '1'" color="lighten-3" class="ma-2" small>
      <translate>created</translate>
    </v-chip>
    <v-chip
      v-else-if="this.status == '2'"
      color="blue lighten-3"
      class="ma-2"
      small
      ><translate>modified</translate>
    </v-chip>
    <v-chip
      v-else-if="this.status == '3'"
      color="light-green lighten-1"
      class="ma-2"
      small
      ><translate>published</translate>
    </v-chip>
    <v-chip
      v-else-if="this.status == '4'"
      color="red lighten-3"
      class="ma-2"
      small
      ><translate>deleted</translate>
    </v-chip>
  </v-card>
</template>

<script>
export default {
  props: ["status"],
};
</script>

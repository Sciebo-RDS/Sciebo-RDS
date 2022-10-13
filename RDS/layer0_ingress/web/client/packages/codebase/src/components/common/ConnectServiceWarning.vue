<template>
    <v-layout column align-center wrap>
      <v-alert dense type="error" class="mb-6">
        Please connect to at least one
        <strong>
          <router-link :to="{ name: 'Services' }">repository</router-link>
        </strong>
        to use RDS.
      </v-alert>
    </v-layout>
</template>

<script>
export default {
    
}
</script>
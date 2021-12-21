<template>
  <v-container>
    <v-card flat>
      <v-card-title>
        <translate>
        Publish your project 
        </translate> 
        </v-card-title>
      <v-card-subtitle>
        <translate>
        Make sure your settings are correct!
        </translate>
      </v-card-subtitle>
      <v-card-text>
        <!-- replace with logic-->
        PortIn: {{ port(project.portIn) }}<br />
        PortOut: {{ port(project.portOut) }}<br />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  props: ["project"],
  methods: {
    port(ports) {
      if (ports.length > 0) {
        return ports[0].port;
      }
      return "";
    },
  },
};
</script>

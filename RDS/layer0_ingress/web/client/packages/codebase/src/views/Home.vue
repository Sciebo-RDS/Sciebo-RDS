<template>
  <Frame :source="frameSource" />
</template>

<script>
// @ is an alias to /src
import Frame from "../components/Frame.vue";

export default {
  name: "Home",
  components: {
    Frame,
  },
  data() {
    return {
      gettingStarted: "https://localhost:8000",
    };
  },
  computed: {
    frameSource() {
      return "/frames/" + this.$config.language + "/welcome.html";
    },
    userHasServicesConnected() {
      //hardcoded filter for owncloud, change
      if (this.userservicelist.length > 1) {
        return true;
      }
      return false;
    },
  },
  mounted() {
    window.addEventListener("message", this.receiveMessage);
  },
  beforeDestroy() {
    window.removeEventListener("message", this.receiveMessage);
  },
  methods: {
    receiveMessage(event) {
      if (event.data.func === "redirect") {
        this.$router.push(event.data.target);
      }
    },
  },
};
</script>

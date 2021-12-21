<template>
  <v-card class="mx-auto pa-4" min-width="400px">
    <v-card-title v-translate>Settings for services</v-card-title>
    <v-select
      v-model="selectedItems"
      :items="servicelist"
      :label="$gettext('Select services')"
      :item-text="(item) => parseServicename(item.servicename)"
      :item-value="(item) => item"
      :value-comparator="(a, b) => a.servicename == b.servicename"
      multiple
    >
      <template v-slot:prepend-item>
        <v-list-item ripple @click="toggle">
          <v-list-item-action>
            <v-icon :color="selectedItems.length > 0 ? 'indigo darken-4' : ''">
              {{ icon }}
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-translate> Select All </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
    </v-select>
    <v-btn
      depressed
      :disabled="!selectedServicesChanged"
      color="error"
      class="mr-3"
      @click="saveSelection"
    >
      <translate>Save selection and activate services</translate>
    </v-btn>
    <v-btn
      depressed
      :disabled="!selectedServicesChanged"
      @click="resetSelection"
    >
      <translate>Cancel service selection</translate>
    </v-btn>
  </v-card>
</template>

<script>
import { mapState } from "vuex";
//import CredentialsInput from "@/components/CredentialsInput";

export default {
  name: "ServiceSelector",
  //components: { CredentialsInput },
  data: () => ({
    selectedItems: [],
  }),
  watch: {
    activatedItems(newVal) {
      this.selectedItems = newVal;
    },
  },
  beforeMount() {
    this.selectedItems = this.activatedItems;
  },
  computed: {
    ...mapState({
      userservicelist: (state) => state.RDSStore.userservicelist,
      servicelist: (state) => state.RDSStore.servicelist,
    }),
    activatedItems: {
      get() {
        return this.userservicelist;
      },
      set(servicelist) {
        // remove not selected services
        for (const service of this.userservicelist) {
          if (!this.containsService(servicelist, service)) {
            this.$store.dispatch("removeService", service);
          }
        }

        // add new services
        // TODO: Trigger oauth2 workflow
        for (const service of this.servicelist) {
          if (!this.containsService(this.userservicelist, service)) {
            this.$store.dispatch("addService", service);
          }
        }

        this.$store.dispatch("requestUserServiceList");
      },
    },
    selectedServicesChanged() {
      return !this.equalServices(this.selectedItems, this.activatedItems);
    },
    selectedAllItems() {
      return this.selectedItems.length === this.servicelist.length;
    },
    selectedSomeItems() {
      return this.selectedItems.length > 0 && !this.selectedAllItems;
    },
    icon() {
      if (this.selectedAllItems) return "mdi-close-box";
      if (this.selectedSomeItems) return "mdi-minus-box";
      return "mdi-checkbox-blank-outline";
    },
  },
  methods: {
    toggle() {
      this.$nextTick(() => {
        if (this.selectedAllItems) {
          this.selectedItems = [];
        } else {
          this.selectedItems = this.servicelist.slice();
        }
      });
    },
    resetSelection() {
      this.$nextTick(() => {
        this.selectedItems = this.activatedItems;
      });
    },
    saveSelection() {
      if (this.selectedItems.length == 0) {
        // change text
      }

      this.activatedItems = this.selectedItems;
    },
  },
};
</script>
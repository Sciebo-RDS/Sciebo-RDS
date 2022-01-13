<template>
  <div v-if="!titleEditMode || !active" class="pt-1">
    <v-div v-if="!!project.researchname" style="overflow:hidden;">
      {{ project.researchname }}
      <v-btn
        v-show="active && project.status < 4"
        class="edit"
        icon
        plain
        color="grey"
        @click.stop="toggleEdit()"
        ><v-icon small>mdi-pencil-outline</v-icon>
      </v-btn>
    </v-div>
    <v-div v-else>
      <translate
        :translate-params="{
          researchIndex: project.researchIndex + 1,
        }"
      >
        Project %{ researchIndex }
      </translate>
      <v-btn
        v-show="active && project.status < 4"
        class="edit"
        icon
        plain
        color="grey"
        @click.stop="toggleEdit()"
        ><v-icon small>mdi-pencil-outline</v-icon>
      </v-btn>
    </v-div>
  </div>
  <div v-else-if="active" style="margin:0px; padding: 0px;">
    <v-div @click.stop="">
      <v-text-field
        @click.stop=""
        @keyup.space.prevent
        @keyup.enter="changeResearchname(project)"
        @keyup.esc="
          toggleEdit();
          newTitle = '';
        "
        :ref="`field${i}`"
        :label="project.researchname"
        placeholder="Enter new title"
        v-model="newTitle"
        counter="50"
        small
        :append-icon="'mdi-content-save-outline'"
        @click:append="changeResearchname(project)"
        class="ma-0 mt-1 pa-0"
      ></v-text-field>
    </v-div>
  </div>
</template>

<style scoped></style>

<script>
export default {
  data() {
    return {
      titleEditMode: false,
    };
  },
  props: ["project", "active"],
  watch: {
    active: function(val) {
      if (!val) {
        this.titleEditMode = false;
        this.newTitle = "";
      }
    },
  },
  methods: {
    toggleEdit() {
      this.titleEditMode = !this.titleEditMode;
    },
    changeResearchname(project) {
      if (this.newTitle.length <= 50) {
        this.newTitle = this.newTitle.trim();
        if (this.newTitle !== project["researchname"]) {
          this.$store.dispatch("changeResearchname", {
            researchIndex: project["researchIndex"],
            researchname: this.newTitle,
          });
          project["researchname"] = this.newTitle;
        }
        this.newTitle = "";
        this.toggleEdit();
      }
    },
  },
};
</script>

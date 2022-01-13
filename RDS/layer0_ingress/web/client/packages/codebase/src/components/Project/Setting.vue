<template>
  <div>
    <template v-if="project.status < 3">
      <v-container>
        <v-row>
          <v-col>
            <ProjectStepper :project="project" />
          </v-col>
        </v-row>

        <v-row align-content="end" justify="space-around">
          <v-col cols="auto" class="mr-auto" />
          <v-col
            v-if="project.status != '3' && project.status != '4'"
            cols="auto"
          >
            <v-btn tile color="error" @click="onDelete(project.researchIndex)">
              <translate>delete project</translate>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </template>
    <template v-else-if="project.status == 3">
      <v-card>
        <v-card-title>
          <translate
            :translate-params="{
              researchIndex: project.researchIndex,
            }"
          >
            Researchindex :%{researchIndex}
          </translate>
        </v-card-title>
        <v-card-subtitle v-translate>
          this is a published project
        </v-card-subtitle>
      </v-card>
    </template>
    <template v-else-if="project.status == 4">
      <v-card>
        <v-card-title>
          <translate
            :translate-params="{
              researchIndex: project.researchIndex,
            }"
          >
            Researchindex :%{researchIndex}
          </translate>
        </v-card-title>
        <v-card-subtitle v-translate>
          this is a deleted project
        </v-card-subtitle>
      </v-card>
    </template>
  </div>
</template>

<script>
import ProjectStepper from "./Stepper.vue";
export default {
  components: {
    ProjectStepper,
  },
  data() {
    return {
      loading: false,
    };
  },
  props: ["project"],
  methods: {
    onDelete(id) {
      this.loading = true;
      this.$emit("delete-project", id);
    },
  },
};
</script>

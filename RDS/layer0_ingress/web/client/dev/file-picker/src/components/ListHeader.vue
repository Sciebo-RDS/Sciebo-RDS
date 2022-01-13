<template>
  <header class="file-picker-header uk-padding-small uk-flex uk-flex-middle uk-flex-between">
    <oc-breadcrumb class="oc-light" :items="breadcrumbsItems" data-testid="breadcrumbs" />
    <div v-if="cancelBtnLabel || isSelectBtnDisplayed">
      <oc-button
        v-if="cancelBtnLabel"
        data-testid="list-header-btn-cancel"
        class="file-picker-btn-cancel uk-margin-small-right"
        @click="cancel"
        v-text="cancelBtnLabel"
      />
      <oc-button
        v-if="isSelectBtnDisplayed"
        data-testid="list-header-btn-select"
        class="file-picker-btn-select-resources"
        variation="primary"
        appearance="filled"
        :disabled="!isSelectBtnEnabled"
        :uk-tooltip="disabledSelectBtnTooltip"
        @click="select"
        v-text="submitBtnLabel"
      />
    </div>
  </header>
</template>

<script>
import path from 'path'

export default {
  name: 'ListHeader',

  props: {
    currentFolder: {
      type: Object,
      required: false,
      default: () => null
    },
    isSelectBtnEnabled: {
      type: Boolean,
      required: true
    },
    isSelectBtnDisplayed: {
      type: Boolean,
      required: false,
      default: true
    },
    selectBtnLabel: {
      type: String,
      required: false,
      default: null
    },
    cancelBtnLabel: {
      type: String,
      required: false,
      default: null
    },
    isLocationPicker: {
      type: Boolean,
      required: true
    },
    areResourcesSelected: {
      type: Boolean,
      required: false,
      default: false
    }
  },

  computed: {
    breadcrumbsItems() {
      const breadcrumbs = []

      if (!this.currentFolder) {
        return breadcrumbs
      }

      const pathSplit = this.currentFolder.path ? this.currentFolder.path.split('/') : ['']

      for (let i = 0; i < pathSplit.length; i++) {
        let itemPath = encodeURIComponent(path.join.apply(null, pathSplit.slice(0, i + 1)))

        breadcrumbs.push({
          index: i,
          text: i === 0 ? this.$gettext('Home') : pathSplit.slice(0, i + 1)[i]
        })

        if (pathSplit.length > 1 && i < pathSplit.length - 1) {
          breadcrumbs[i].onClick = () => this.openFolder(itemPath || '/')
        }
      }

      return breadcrumbs
    },

    disabledSelectBtnTooltip() {
      if (this.isSelectBtnEnabled) {
        return null
      }

      return this.$gettext(
        'Please, select at least one resource. You can select a resource by clicking on its row or via its checkbox.'
      )
    },

    submitBtnLabel() {
      if (this.selectBtnLabel) {
        return this.selectBtnLabel
      }

      if (this.isLocationPicker) {
        return this.areResourcesSelected
          ? this.$gettext('Select folder')
          : this.$gettext('Select current folder')
      }

      return this.$gettext('Select resources')
    }
  },

  methods: {
    openFolder(path) {
      this.$emit('openFolder', path)
    },

    select() {
      this.$emit('select')
    },

    cancel() {
      this.$emit('cancel')
    }
  }
}
</script>

<template>
  <div class="uk-flex uk-height-1-1 uk-flex-column uk-overflow-hidden">
    <list-header
      :current-folder="currentFolder"
      :is-select-btn-enabled="isSelectBtnEnabled"
      :is-select-btn-displayed="isSelectBtnDisplayed"
      :is-location-picker="isLocationPicker"
      :are-resources-selected="areResourcesSelected"
      :select-btn-label="selectBtnLabel"
      :cancel-btn-label="cancelBtnLabel"
      @openFolder="loadFolder"
      @select="emitSelectBtnClick"
      @cancel="emitCancel"
    />
    <div
      v-if="state === 'loading'"
      key="loading-message"
      class="uk-flex uk-flex-1 uk-flex-middle uk-flex-center"
    >
      <oc-spinner :aria-label="$gettext('Loading resources')" />
    </div>
    <list-resources
      v-if="state === 'loaded'"
      key="resources-list"
      class="uk-flex-1 oc-border"
      :resources="resources"
      :is-location-picker="isLocationPicker"
      @openFolder="loadFolder"
      @selectResources="selectResources"
      @selectLocation="emitSelectBtnClick"
    />
  </div>
</template>

<script>
import { buildResource } from '@/helpers/resources'
import ListResources from './ListResources.vue'
import ListHeader from './ListHeader.vue'

import MixinAccessibility from '@/mixins/accessibility'

export default {
  name: 'FilePicker',

  components: {
    ListHeader,
    ListResources
  },

  mixins: [MixinAccessibility],

  props: {
    variation: {
      type: String,
      required: true,
      validator: (value) => value === 'resource' || 'location'
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
    isSelectBtnDisplayed: {
      type: Boolean,
      required: false,
      default: true
    },
    isInitialFocusEnabled: {
      type: Boolean,
      required: false,
      default: false
    }
  },

  data: () => ({
    state: 'loading',
    resources: [],
    currentFolder: null,
    selectedResources: [],
    davProperties: [
      '{http://owncloud.org/ns}permissions',
      '{http://owncloud.org/ns}favorite',
      '{http://owncloud.org/ns}fileid',
      '{http://owncloud.org/ns}owner-id',
      '{http://owncloud.org/ns}owner-display-name',
      '{http://owncloud.org/ns}share-types',
      '{http://owncloud.org/ns}privatelink',
      '{DAV:}getcontentlength',
      '{http://owncloud.org/ns}size',
      '{DAV:}getlastmodified',
      '{DAV:}getetag',
      '{DAV:}resourcetype'
    ],
    isInitial: true
  }),

  computed: {
    isSelectBtnEnabled() {
      return this.isLocationPicker || this.areResourcesSelected
    },

    isLocationPicker() {
      return this.variation === 'location'
    },

    areResourcesSelected() {
      return this.selectedResources.length > 0
    }
  },

  created() {
    this.loadFolder('/')
  },

  methods: {
    loadFolder(path) {
      this.state = 'loading'

      this.$client.files
        .list(decodeURIComponent(path), 1, this.davProperties)
        .then((resources) => {
          resources = resources.map((resource) => buildResource(resource))
          this.resources = resources.splice(1)
          this.currentFolder = resources[0]

          if (this.isLocationPicker) {
            this.$emit('update', [this.currentFolder])
          }

          this.$emit('folderLoaded', this.currentFolder)

          this.state = 'loaded'

          if ((this.isInitial && this.isInitialFocusEnabled) || !this.isInitial) {
            this.$nextTick(() =>
              this.$_accessibility_focusAndAnnounceBreadcrumb(this.resources.length)
            )
          }

          this.isInitial = false
        })
        .catch((error) => {
          console.error(error)

          this.state = 'failed'
        })
    },

    selectResources(resources) {
      this.selectedResources = resources
      this.$emit('update', resources)
    },

    emitSelectBtnClick() {
      const resources =
        this.selectedResources.length < 1 && this.isLocationPicker
          ? [this.currentFolder]
          : this.selectedResources

      this.$emit('select', resources)
    },

    emitCancel() {
      this.$emit('cancel')
    }
  }
}
</script>

export default {
  computed: {
    isPersonalRoute() {
      return this.$route.name === 'files-personal'
    },
    isFavoritesRoute() {
      return this.$route.name === 'files-favorites'
    },
    isTrashbinRoute() {
      return this.$route.name === 'files-trashbin'
    },
    isSharedWithMeRoute() {
      return this.$route.name === 'files-shared-with-me'
    },
    isSharedWithOthersRoute() {
      return this.$route.name === 'files-shared-with-others'
    },
    isAnySharedWithRoute() {
      return this.isSharedWithMeRoute || this.isSharedWithOthersRoute
    },
    isPublicFilesRoute() {
      return this.$route.name === 'files-public-list'
    },
    isPublicPage() {
      if (this.$route.meta) {
        return this.$route.meta.auth === false
      }
      return false
    }
  }
}

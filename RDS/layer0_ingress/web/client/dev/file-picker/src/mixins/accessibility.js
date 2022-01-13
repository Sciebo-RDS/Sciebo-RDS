export default {
  methods: {
    $_accessibility_focusAndAnnounceBreadcrumb(itemsCount) {
      const activeBreadcrumb = document.querySelector(
        '.oc-breadcrumb-list-item span[aria-current="page"]'
      )

      if (!activeBreadcrumb) {
        return
      }

      const translated = this.$ngettext(
        'This folder contains 1 item.',
        'This folder contains %{ itemsCount } items.',
        itemsCount
      )
      const announcement =
        itemsCount > 0
          ? this.$gettextInterpolate(translated, { itemsCount })
          : this.$gettext('This folder has no content.')
      const invisibleHint = document.createElement('p')

      invisibleHint.className = 'oc-invisible-sr oc-breadcrumb-sr'
      invisibleHint.innerHTML = announcement

      activeBreadcrumb.append(invisibleHint)
      activeBreadcrumb.focus()
    }
  }
}

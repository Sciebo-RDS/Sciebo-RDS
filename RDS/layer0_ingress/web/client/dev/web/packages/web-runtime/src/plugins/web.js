import { mapGetters, mapActions } from 'vuex'

import { encodePath } from 'web-pkg/src/utils'

export default {
  install(Vue) {
    Vue.mixin({
      computed: {
        ...mapGetters(['getToken', 'isAuthenticated', 'capabilities']),
        ...mapGetters('Files', ['publicLinkPassword']),
        ...mapGetters(['configuration']),

        currentExtension() {
          return this.$route.path.split('/')[1]
        },

        isUrlSigningEnabled() {
          return this.capabilities.core && this.capabilities.core['support-url-signing']
        }
      },
      methods: {
        ...mapActions('Files', ['addActionToProgress', 'removeActionFromProgress']),
        ...mapActions(['showMessage']),

        publicPage() {
          // public page is either when not authenticated
          // but also when accessing pages that require no auth even when authenticated
          return !this.isAuthenticated || this.$route.meta.auth === false
        },
        // FIXME: optional publicContext parameter is a mess
        async downloadFile(file, publicContext = null, version = null) {
          const publicPage = publicContext !== null ? publicContext : this.publicPage()

          // construct the url and headers
          let url = null
          let headers = {}
          if (publicPage) {
            url = file.downloadURL
          } else {
            if (version === null) {
              url = this.$client.helpers._webdavUrl + file.path
            } else {
              url = this.$client.fileVersions.getFileVersionUrl(file.id, version)
            }
            headers = { Authorization: 'Bearer ' + this.getToken }
          }

          // download with signing enabled
          if (!publicPage && this.isUrlSigningEnabled) {
            try {
              const response = await fetch(url, {
                method: 'HEAD',
                headers
              })
              if (response.status === 200) {
                const signedUrl = await this.$client.signUrl(url)
                this.triggerDownload(signedUrl, file.name)
                return
              }
            } catch (e) {
              console.log(e)
            }
            this.showMessage({
              title: this.$gettext('Download failed'),
              desc: this.$gettext('File could not be located'),
              status: 'danger',
              autoClose: {
                enabled: true
              }
            })
            return
          }

          this.triggerDownload(url, file.name)
        },

        /**
         * Checks whether the browser is Internet Explorer 11
         * @return {boolean} true if the browser is Internet Explorer 11
         */
        isIE11() {
          return !!window.MSInputMethodContext && !!document.documentMode
        },
        encodePath,
        triggerDownload(url, name) {
          const a = document.createElement('a')
          a.style.display = 'none'
          document.body.appendChild(a)
          a.href = url
          // use download attribute to set desired file name
          a.setAttribute('download', name)
          // trigger the download by simulating click
          a.click()
          // cleanup
          document.body.removeChild(a)
        }
      }
    })
  }
}

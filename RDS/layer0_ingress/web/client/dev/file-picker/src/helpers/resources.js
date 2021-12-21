import { uniqueId, chain } from 'lodash'
import fileTypeIconMappings from './fileTypeIconMappings.json'
import path from 'path'

function _extName(fileName) {
  let ext = ''
  const ex = fileName.match(/\.[0-9a-z]+$/i)
  if (ex) {
    ext = ex[0].substr(1)
  }
  return ext
}

export function buildResource(resource) {
  const ext = resource.type !== 'dir' ? _extName(resource.name) : ''
  return {
    type: resource.type === 'dir' ? 'folder' : resource.type,
    // actual file id (string)
    id: resource.fileInfo['{http://owncloud.org/ns}fileid'],
    // temporary list id, to be used for view only and for uniqueness inside the list
    viewId: uniqueId('file-'),
    starred: resource.fileInfo['{http://owncloud.org/ns}favorite'] !== '0',
    mdate: resource.fileInfo['{DAV:}getlastmodified'],
    size: (function () {
      if (resource.type === 'dir') {
        return resource.fileInfo['{http://owncloud.org/ns}size']
      } else {
        return resource.fileInfo['{DAV:}getcontentlength']
      }
    })(),
    extension: (function () {
      return ext
    })(),
    name: path.basename(resource.name),
    path: resource.name,
    permissions: resource.fileInfo['{http://owncloud.org/ns}permissions'] || '',
    etag: resource.fileInfo['{DAV:}getetag'],
    sharePermissions:
      resource.fileInfo['{http://open-collaboration-services.org/ns}share-permissions'],
    shareTypes: (function () {
      let shareTypes = resource.fileInfo['{http://owncloud.org/ns}share-types']
      if (shareTypes) {
        shareTypes = chain(shareTypes)
          .filter(
            (xmlvalue) =>
              xmlvalue.namespaceURI === 'http://owncloud.org/ns' &&
              xmlvalue.nodeName.split(':')[1] === 'share-type'
          )
          .map((xmlvalue) => parseInt(xmlvalue.textContent || xmlvalue.text, 10))
          .value()
      }
      return shareTypes || []
    })(),
    privateLink: resource.fileInfo['{http://owncloud.org/ns}privatelink'],
    owner: {
      username: resource.fileInfo['{http://owncloud.org/ns}owner-id'],
      displayName: resource.fileInfo['{http://owncloud.org/ns}owner-display-name']
    },
    canUpload: function () {
      return this.permissions.indexOf('C') >= 0
    },
    canDownload: function () {
      return this.type !== 'folder'
    },
    canBeDeleted: function () {
      return this.permissions.indexOf('D') >= 0
    },
    canRename: function () {
      return this.permissions.indexOf('N') >= 0
    },
    canShare: function () {
      return this.permissions.indexOf('R') >= 0
    },
    canCreate: function () {
      return this.permissions.indexOf('C') >= 0
    },
    isMounted: function () {
      return this.permissions.indexOf('M') >= 0
    },
    isReceivedShare: function () {
      return this.permissions.indexOf('S') >= 0
    }
  }
}

export function getResourceIcon(resource) {
  if (resource) {
    if (resource.type === 'folder') {
      return 'folder'
    }
    const icon = fileTypeIconMappings[resource.extension.toLowerCase()]
    if (icon) return `${icon}`
  }
  return 'x-office-document'
}

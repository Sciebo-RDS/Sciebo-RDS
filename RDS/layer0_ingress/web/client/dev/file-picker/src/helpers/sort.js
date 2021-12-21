import { naturalSortCompare } from './textUtils'

export function sortByName(resource1, resource2) {
  if (resource1.type === 'folder' && resource2.type !== 'folder') {
    return -1
  }

  if (resource1.type !== 'folder' && resource2.type === 'folder') {
    return 1
  }

  return naturalSortCompare(resource1.name, resource2.name)
}

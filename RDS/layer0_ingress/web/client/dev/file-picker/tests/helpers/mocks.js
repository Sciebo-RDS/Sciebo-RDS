import resources from '../fixtures/resources'

export const listResources = (path) => {
  return new Promise((resolve) => {
    resolve(resources[path])
  })
}

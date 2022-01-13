/**
 * Identify which way of configuring the file picker was chosen and return a config object from it,
 * either by fetching, parsing or plain returning it.
 *
 * @param configObject object|string|null Either an object or a json string holding the config
 * @param configLocation string A config url
 * @returns {Promise<any>}
 */
export async function loadConfig(configObject, configLocation) {
  if (configObject === null) {
    const config = await fetch(configLocation)
    return await config.json()
  }

  if (typeof configObject === 'string') {
    return JSON.parse(configObject)
  }

  return configObject
}

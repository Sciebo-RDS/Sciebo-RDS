import { loadConfig } from '@/helpers/config'

const exampleConfig = {
  server: 'https://own.cloud/',
  auth: {
    clientId: 'rWgSlOtLJCO6QBtEVgDdXWlUOrEt2CBL9F48c6TQKt3ZGG5ofazNhEJjp6TlyanT',
    url: 'https://own.cloud/index.php/apps/oauth2/api/v1/token',
    authUrl: 'https://own.cloud/index.php/apps/oauth2/authorize'
  }
}

describe('FilePicker config', () => {
  describe('loadConfig', () => {
    it('When no configObject is provided, then the config is fetched from the configLocation', async () => {
      fetch.mockResponseOnce(JSON.stringify(exampleConfig))
      const config = await loadConfig(null, 'https://whatever.location/config.json')
      expect(config).toEqual(exampleConfig)
    })
    it('When a configObject is provided and of type string, it is parsed as JSON', async () => {
      const config = await loadConfig(JSON.stringify(exampleConfig), null)
      expect(config).toEqual(exampleConfig)
    })
    it('When a configObject is provided and not of type string, it is returned without modification', async () => {
      const config = await loadConfig(exampleConfig, null)
      expect(config).toEqual(exampleConfig)
    })
  })
})

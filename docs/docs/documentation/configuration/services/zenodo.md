# Zenodo

Please refer to the [Setting up Zenodo](../../../gettingstarted/zenodo.md) page of our Getting Started guide.
All options for your `values.yaml` can be found in the next section.

## Advanced `values.yaml`

```yaml
layer1-port-zenodo: # zenodo`s specific options
  enabled: true # here you could disable it, but who would like to do it?
  environment: # needs to be adjusted to correct values
    ADDRESS: https://sandbox.zenodo.org # the testing instance
    #ADDRESS: https://zenodo.org # the main instance
    OAUTH_CLIENT_ID: ABC # given by the OAUTH process of the used zenodo instance from above.
    OAUTH_CLIENT_SECRET: XYZ # given by the OAUTH process of the used zenodo instance from above.
```

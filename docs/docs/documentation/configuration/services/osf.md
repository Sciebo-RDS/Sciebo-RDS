---

id: osf
---

# OSF

First, you need to create a separate application in [osf](https://test.osf.io/settings/applications) for sciebo RDS. Set a name, project homepage and a description. The most important field is `Authorization callback URL`, which have to be the instance for sciebo RDS `your-rds.institution.org`. After submitting the information, you will get the `Client ID` and `Client secret`. Place it in your `values.yaml`. The required configuration in your `values.yaml` to get the OSF connector up can be found in the next section.

## Advanced `values.yaml`

```yaml
layer1-port-openscienceframework: # the osf connector
  enabled: true # enable OSF
  environment:
    ADDRESS: https://accounts.test.osf.io # the testing instance
    #ADDRESS: https://accounts.osf.io # the main istance
    API_ADDRESS: https://api.test.osf.io/v2 # the testing instance
    #API_ADDRESS: https://api.osf.io/v2 # the main instance
    OAUTH_CLIENT_ID: ABC # the oauth client_id given by osf oauth service
    OAUTH_CLIENT_SECRET: XYZ # the oauth client_secret given by osf oauth service
```
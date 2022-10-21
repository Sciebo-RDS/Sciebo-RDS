---

id: osf
---

# OSF

1. [Create an OSF Test application](https://test.osf.io/settings/applications) to get API access for your sciebo RDS instance. 
Set a name, project homepage and a description. The most important field is `Authorization callback URL`, which has to match the domain of your sciebo RDS instance (e.g. `your-rds.institution.org`).
2. The first step will give you an OSF `Client ID` and `Client secret`.   
Place it in your `values.yaml` as shown beneath.

## `values.yaml`

```yaml
[...]

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
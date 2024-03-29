# Advanced `values.yaml` File

The yaml file shown below is an exhaustive list of all settings introduced by sciebo RDS.

Further options are available through dependencies, which are linked within the listing. 
A lot of the settings are optional, as you can see when you compare it to the minimal `values.yaml` file shown in the [getting started guide](./../../gettingstarted/kubernetes.md#helm).


```yaml
global:
  # creates a namespace on its own
  namespace: 
    create: false
    name: research-data-services
  # will be used for ingress host
  # edit here if you changed it in create_certs.sh and wants to use another domain
  #ingress:
  #  tls:
  #    secretName: sciebords-tls-public
  rds:
    domain: your-rds.institution.org
  describo:
    api_secret: IAMSECRET
    domain: your-describo.institution.org
  # Domains you want to use as input, currently only owncloud supported,
  # this enables to use multiple owncloud instances with a single sciebo RDS
  domains:
    - name: owncloud.local # name needs to be exact the same as the second part after last @ in the cloudId
      ADDRESS: https://owncloud.local/owncloud
      OAUTH_CLIENT_ID: ABC
      OAUTH_CLIENT_SECRET: XYZ
      filters: # filters are helpful, if you want to use the same sciebo RDS instance for multiple cloudstorage installations.
        # After filters are applied, you have a set of service which are listed in "only" (if empty, it means all services available in sciebo RDS) without all services in "except" (if empty, it means no services)
        only:
          - layer1-port-openscienceframework
        except:
          - layer1-port-datasafe
      SUPPORT_EMAIL: mail@side.com
      MANUAL_URL: usermanual.side.com
# Set this to DEBUG and restart your applications to get more informations in logs. Default: INFO
loglevel: INFO
# If you set this to "False", SSL will not be verified in all https requests. Default: "True"
verify_ssl: "True"
proxy:
  http_proxy: "''"
  https_proxy: "''"
  no_proxy: layer1-port-owncloud,layer1-port-zenodo,layer1-port-openscienceframework,layer1-port-reva,layer2-port-service,layer3-token-storage,layer3-research-manager
layer0-describo:
  enabled: true
  # Postgresql configuration options https://artifacthub.io/packages/helm/bitnami/postgresql/10.14.3
  postgresql:
    # starts its own postgresql database.
    postgresqlDatabase: describo
    postgresqlUsername: admin
    postgresqlPassword: admin
  # describo needs a separate domain from sciebords. set the exact same value later in layer0-web for VUE_APP_DESCRIBO_URL
  domain: separate-domain-for-describo.your-institution.org
  environment:
    ADMIN_PASSWORD: your-admin-password
    LOG_LEVEL: "info"
layer0-helper-describo-token-updater:
  enabled: true
  environment: {}
    # advanced settings
    # DESCRIBO_API_ENDPOINT: http://layer0-describo/api/session/application
layer0-web:
  enabled: true
  environment:
    # the password, which will be used to encrypt all user data
    SECRET_KEY: 1234
    # should be changed to all known access origins to sciebo RDS backend. e.g. web proxies
    # Onwcloud-Domains will be included automatically from global.domains in bootup process.
    # FLASK_ORIGINS:
    #   [
    #     "http://localhost:8080",
    #   ]
    # advanced settings
    EMBED_MODE: true
    # DESCRIBO_API_ENDPOINT: http://layer0-describo/api/session/application
layer1-port-owncloud:
  # ownCloud will be configured through global.domains, because this way you need to configure it only once
  enabled: true
layer1-port-zenodo:
  enabled: true
  environment:
    # needs to be adjusted to correct values
    ADDRESS: https://sandbox.zenodo.org
    OAUTH_CLIENT_ID: ABC
    OAUTH_CLIENT_SECRET: XYZ
layer1-port-openscienceframework:
  enabled: true
  environment:
    ADDRESS: https://accounts.test.osf.io
    API_ADDRESS: https://api.test.osf.io/v2
    # needs to be adjusted to correct values
    OAUTH_CLIENT_ID: ABC
    OAUTH_CLIENT_SECRET: XYZ
layer2-exporter-service: {}
layer2-port-service:
  environment:
    TOKENSERVICE_STATE_SECRET: ABC
    IGNORE_PROJECTS: True # this ignores the pull algo for external projects
layer2-metadata-service: {}
layer3-research-manager: {}
layer3-token-storage: {}
feature:
  jaeger: false
# see: https://github.com/bitnami/charts/tree/master/bitnami/redis-cluster
# Redis-helper configuration options https://artifacthub.io/packages/helm/bitnami/redis/16.10.1
redis-helper: {}
# Redis configuration options https://artifacthub.io/packages/helm/bitnami/redis-cluster/7.6.1
redis:
  cluster: {}
  redis:
    config: {}
# see: https://github.com/jaegertracing/helm-charts
jaeger: {}
```

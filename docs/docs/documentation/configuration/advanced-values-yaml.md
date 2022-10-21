# Advanced `values.yaml` File

The yaml file shown below is an exhaustive list of all settings introduced by sciebo RDS.

Further options are available through dependencies, which are linked within the listing. 
A lot of the settings are optional, as you can see when you compare it to the minimal `values.yaml` file shown in the [getting started guide](./../../gettingstarted/kubernetes.md#helm).


```yaml
global:
  image:
    tag: v0.1.9 # has to be the same as the tag of the Owncloud plugin
  namespace: # kubernetes separates applications in namespaces
    create: false # creates a namespace on its own
    name: "rds" # the name of the namespace that will be used and / or created for sciebo RDS.
  #ingress: # enable this, if you want to set a custom tls certificate
  #  tls:
  #    secretName: sciebords-tls-public
  rds:
    domain: your-rds.institution.org # the domain you created for the sciebo rds ui
  describo: # all information necessary for describo
    api_secret: IAMSECRET # the Describo api password, necessary for all requests against the api
    domain: your-describo.institution.org # the domain you created for describo ui
  # Domains you want to use as input, currently only owncloud is supported,
  # this enables you to use multiple owncloud instances with a single sciebo RDS
  domains:
    - name: owncloud.local # name needs to be exactly the same as the second part after last @ in the cloudId
      ADDRESS: https://owncloud.local/owncloud # set this to the domain corresponding to the name value before
      OAUTH_CLIENT_ID: ABC # client_id of oauth service provider
      OAUTH_CLIENT_SECRET: XYZ # client_secret of oauth service provider
      filters: # filters are helpful if you want to use the same sciebo RDS instance for multiple cloudstorage installations. 
        # After filters are applied, you have a set of services that are listed in "only" 
        only: # if this list isn't empty, only the services in this list will be available
          - "layer1-port-openscienceframework"
        except: # the services in this list will not be available
          - "layer1-port-datasafe"
loglevel: INFO # Set this to DEBUG and restart your applications to get more detailed logs. Default: INFO
verify_ssl: "True" # If this is set to "False", SSL will not be verified in all https requests. Default: "True"
proxy: # proxy for http requests
  http_proxy: "''"
  https_proxy: "''"
layer0-describo:
  enabled: true # enables or disable describo
  # Postgresql configuration options https://artifacthub.io/packages/helm/bitnami/postgresql/10.14.3
  postgresql: # starts its own postgresql database.
    postgresqlDatabase: describo
    postgresqlUsername: admin
    postgresqlPassword: admin
  domain: separate-domain-for-describo.your-institution.org # describo needs a separate domain from sciebords. set the exact same value later in layer0-web for VUE_APP_DESCRIBO_URL
  environment:
    LOG_LEVEL: info # set debugging detail level
    ADMIN_PASSWORD: IAMSECRET
layer0-helper-describo-token-updater: # this is a helper component to communicate with describo
  enabled: true
  environment: {}
    # advanced settings
    # DESCRIBO_API_ENDPOINT: http://layer0-describo/api/session/application
layer0-web:
  enabled: true
  environment:
    SECRET_KEY: 1234 # the password that will be used to encrypt all user data.
    # The following should be changed to all known access origins to sciebo RDS backend. e.g. web proxies
    # Onwcloud-Domains will be included automatically from global.domains in bootup process.
    # FLASK_ORIGINS:
    #   [
    #     "http://localhost:8080",
    #   ]
    EMBED_MODE: true # Decides if sciebo RDS will be run in embed mode (wrapped as a plugin) or standalone. Standalone is not tested very well.
    # DESCRIBO_API_ENDPOINT: http://layer0-describo/api/session/application # here you can change the api endpoint used for describo (if you want to host it elsewhere).
layer1-port-owncloud: # ownCloud will be configured through global.domains further above, this way you only need to configure it once
  enabled: true # but it can be disabled globally here
layer1-port-zenodo: # the zenodo connector. 
  enabled: true
  environment:
    # needs to be adjusted to correct (production) values
    ADDRESS: https://sandbox.zenodo.org
    OAUTH_CLIENT_ID: ABC # given by the zenodo oauth page
    OAUTH_CLIENT_SECRET: XYZ # given by the zenodo oauth page
layer1-port-openscienceframework: # the osf connector
  enabled: true # enable OSF
  environment:
    ADDRESS: https://accounts.test.osf.io # set to correct value - the production instance is accounts.osf.io
    API_ADDRESS: https://api.test.osf.io/v2 # needs to be adjusted to correct values - production instance is accounts.osf.io
    OAUTH_CLIENT_ID: ABC # the oauth client_id given by osf oauth service
    OAUTH_CLIENT_SECRET: XYZ # the oauth client_secret given by osf oauth service
layer2-exporter-service: {} # the service which handles exporting - default helm options available - like labels, service or resources
layer2-port-service: # the service which handles misc functions
  environment:
    TOKENSERVICE_STATE_SECRET: ABC # use a unique secret to encrypt stored informations. If not set, it uses a default one. 
    IGNORE_PROJECTS: "True" # this ignores the pull algo for external projects. It speeds up the whole system by alot. But reduces metadata informations
layer2-metadata-service: {} # the service for metadata - default helm options available - like labels, service or resources
layer3-research-manager: {} # storage for the internal research object - default helm options available - like labels, service or resources
layer3-token-storage: {} # storage for oauth tokens - default helm options available - like labels, service or resources
feature:
  jaeger: false # if you want to use jaeger, enable it here.
redis-helper: {} # Redis-helper configuration options https://artifacthub.io/packages/helm/bitnami/redis/16.10.1
redis: # Redis configuration options https://artifacthub.io/packages/helm/bitnami/redis-cluster/7.6.1
  cluster: {}
  redis:
    config: {}
jaeger: {} # see: https://github.com/jaegertracing/helm-charts
```
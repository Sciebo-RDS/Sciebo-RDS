# Advanced Values.yaml File

The yaml file listed below shows all options introduced by sciebo RDS. More options are available through dependencies, which are linked within the listing. 
A lot of the options are not needed, as you saw in the getting started guide. But because it is a full listing, they will be shown here.


```yaml
global:
  image:
    tag: v0.1.9 # set the same tag here as the same you used before for Owncloud
  namespace: # kubernetes separates applications in namespaces
    create: false # creates a namespace on its own
    name: "rds" # the name of the namespace, which will be used for sciebo RDS and / or created.
  #ingress: # enable this, if you want to set a custom tls certificate
  #  tls:
  #    secretName: sciebords-tls-public
  rds:
    domain: your-rds.institution.org # the domain you created for the sciebo rds ui
  describo: # all needed informations for describo
    api_secret: IAMSECRET # the api password, which is needed for all requests against the api
    domain: your-describo.institution.org # the domain you created for describo ui
  # Domains you want to use as input, currently only owncloud supported,
  # this enables to use multiple owncloud instances with a single sciebo RDS
  domains:
    - name: owncloud.local # name needs to be exact the same as the second part after last @ in the cloudId
      ADDRESS: https://owncloud.local/owncloud # set this to the corresponding domain to the name value before
      OAUTH_CLIENT_ID: ABC # client_id from oauth service provider
      OAUTH_CLIENT_SECRET: XYZ # client_secret from oauth service provider
      filters: # filters are helpful, if you want to use the same sciebo RDS instance for multiple cloudstorage installations.
        only: # this filters all services without this names 
          - "layer1-port-openscienceframework"
        except: # this filters all services with this names
          - "layer1-port-datasafe"
loglevel: INFO # Set this to DEBUG and restart your applications to get more informations in logs. Default: INFO
verify_ssl: "True" # If you set this to "False", SSL will not be verified in all https requests. Default: "True"
proxy: # set proxy for http requests
  http_proxy: "''"
  https_proxy: "''"
layer0-describo:
  enabled: true # this enables describo
  # Postgresql configuration options https://artifacthub.io/packages/helm/bitnami/postgresql/10.14.3
  postgresql: # starts its own postgresql database.
    postgresqlDatabase: "describo"
    postgresqlUsername: "admin"
    postgresqlPassword: "admin"
  domain: separate-domain-for-describo.your-institution.org # describo needs a separate domain from sciebords. set the exact same value later in layer0-web for VUE_APP_DESCRIBO_URL
  environment:
    LOG_LEVEL: "info" # set debugging informations level
layer0-helper-describo-token-updater: # this is a helper component to communicate with describo
  enabled: true
  environment: {}
    # advanced settings
    # DESCRIBO_API_ENDPOINT: http://layer0-describo/api/session/application
layer0-web:
  enabled: true
  environment:
    SECRET_KEY: 1234 # the password, which will be used to encrypt all user data
    # the following should be changed to all known access origins to sciebo RDS backend. e.g. web proxies
    # Onwcloud-Domains will be included automatically from global.domains in bootup process.
    # FLASK_ORIGINS:
    #   [
    #     "http://localhost:8080",
    #   ]
    EMBED_MODE: true # this set the mode, if sciebo RDS will be run in embed mode (behind a plugin) or standalone. Standalone is not tested very well.
    # DESCRIBO_API_ENDPOINT: http://layer0-describo/api/session/application # here you can change the used describo api endpoint, if you want to host it whereelse.
layer1-port-owncloud: # ownCloud will be configured through global.domains further above, because this way you need to configure it only once
  enabled: true # but it can be disabled globally here
layer1-port-zenodo: # the zenodo connector. 
  enabled: true
  environment:
    # needs to be adjusted to correct values
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
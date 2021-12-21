# Sciebo RDS Helm Charts

This repo holds all charts for the sciebo rds microservices.

## Usage

Add this charts to your repository list.

```bash
helm repo add sciebo-rds https://www.research-data-services.org/charts/
```

Verify that the repo finds the charts

```bash
helm search repo sciebo-rds
```

## Install the whole system

If you want to install the whole system, you can use the *all* chart, which depends on all services. You have to specify a values.yaml file to set all required parameters.

The following commands will add the needed repository, add a values.yaml file and opens it with vi. After you enter your credentials, it will try to install the chart with all services under the name "sciebo-rds" in your configured cluster.

```bash
helm repo add sciebo-rds https://www.research-data-services.org/charts/
cat > values.yaml <<EOF
global:
  # will be used for ingress host
  # edit here if you changed it in create_certs.sh and wants to use another domain
  domain: rds.local
  ingress:
    tls:
      secretName: sciebords-tls-public

# Set this to DEBUG and restart your applications to get more informations in logs. Default: INFO
loglevel: INFO
# If you set this to "False", SSL will not be verified in all https requests. Default: "True"
verify_ssl: "True"
# The URL, which you configured in your oauth providers
rds_oauth_redirect_uri: https://owncloud.local/index.php/apps/rds/oauth
proxy:
  http_proxy: ""
  https_proxy: ""
  no_proxy: circle1-port-owncloud,circle1-port-zenodo,circle1-port-openscienceframework,circle1-port-reva,circle2-port-service,circle3-token-storage,circle3-research-manager
namespace: # creates a namespace on their own, if you wants to
  create: false
  name: "research-data-services"

layer0-describo:
  enabled: true
  image:
    tag: main
  environment:
    EMBED_MODE: true
  postgresql:
    postgresqlDatabase: "describo"
    postgresqlUsername: "admin"
    postgresqlPassword: "admin"
    persistance:
      storageClassName: cinderbronze-delete
layer0-web:
  enabled: true
  image:
    tag: main
  environment:
    EMBED_MODE: true
    FLASK_ORIGINS: ["http://localhost:8080", "http://localhost:8085", "http://localhost:8000", "http://localhost:9100"]
    SECRET_KEY: 1234
    OWNCLOUD_URL: http://localhost:8000
    OWNCLOUD_OAUTH_CLIENT_ID: ABC
    OWNCLOUD_OAUTH_CLIENT_SECRET: XYZ
    OWNCLOUD_OAUTH_CLIENT_REDIRECT: https://<your-rds-installation>
    OWNCLOUD_OAUTH_CLIENT_AUTHORIZE_URL: http://localhost:8000/apps/oauth2/authorize
    DESCRIBO_API_ENDPOINT: http://localhost:9000/api/session/application
    DESCRIBO_API_SECRET: IAMSECRET
circle1-port-owncloud:
  enabled: false
  environment:
    # needs to be adjusted to correct values
    ADDRESS: https://owncloud.local/owncloud
    OAUTH_CLIENT_ID: ABC
    OAUTH_CLIENT_SECRET: XYZ
circle1-port-zenodo:
  enabled: false
  environment:
    # needs to be adjusted to correct values
    ADDRESS: https://sandbox.zenodo.org
    OAUTH_CLIENT_ID: ABC
    OAUTH_CLIENT_SECRET: XYZ
circle1-port-openscienceframework:
  enabled: false
  environment:
    ADDRESS: https://accounts.test.osf.io
    API_ADDRESS: https://api.test.osf.io/v2
    # needs to be adjusted to correct values
    OAUTH_CLIENT_ID: ABC
    OAUTH_CLIENT_SECRET: XYZ
circle2-exporter-service: {}
circle2-port-service: {}
circle2-metadata-service: {}
circle3-research-manager: {}
circle3-token-storage: {}
# see: https://github.com/bitnami/charts/tree/master/bitnami/redis-cluster
redis:
  cluster: {}
  redis:
    config: {}
# see: https://github.com/jaegertracing/helm-charts
jaeger: {}
EOF
vi values.yaml
helm upgrade sciebo-rds sciebo-rds/all --install --values values.yaml
```

The following table lists the most used configurable parameters of the Sciebo RDS chart and their default values.

| Parameter                                                     | Description                                                                      | Default                                              |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `global.domain`                                               |                                                                                  | https://localhost                                    |
| `global.REDIS_HOST`                                           | This redis host will be used to store values. Redis-Cluster instance             | redis                                                |
| `global.REDIS_PORT`                                           | This redis port will be used to store values. Redis-Cluster instance             | 6379                                                 |
| `global.REDIS_HELPER_HOST`                                    | This redis host will be used to store values. Standalone redis (Purpose: Pubsub) | redis                                                |
| `global.REDIS_HELPER_HOST`                                    | This redis port will be used to store values. Standalone redis (Purpose: Pubsub) | 6379                                                 |
| `global.ingress.tls.secretName`                               | The name of the tls secret within k8s.                                           | "sciebords-tls-public"                               |
| `circle1-port-zenodo.environment.ZENODO_ADDRESS`              |                                                                                  | https://sandbox.zenodo.org                           |
| `circle1-port-zenodo.environment.ZENODO_OAUTH_CLIENT_ID`      | Required                                                                         |                                                      |
| `circle1-port-zenodo.environment.ZENODO_OAUTH_CLIENT_SECRET`  | Required                                                                         |                                                      |
| `circle1-port-owncloud.environment.OWNCLOUD_INSTALLATION_URL` |                                                                                  | https://localhost/owncloud                           |
| `circle1-port-owncloud.environment.OWNCLOUD_OAUTH_CLIENT_ID`  | Required                                                                         |                                                      |
| `circle1-port-owncloud.environment.`                          | Required                                                                         |                                                      |
| `<circle3-COMPONENT>.environment.IN_MEMORY_AS_FAILOVER`       | If no redis was found, service crashes. With "True" it uses inmemory.            | "False"                                              |
| `redis`                                                       | See [Dependencies](#Dependencies)                                                |                                                      |
| `jaeger`                                                      | See [Dependencies](#Dependencies)                                                |                                                      |
| `<component>.replicaCount`                                    |                                                                                  | 1                                                    |
| `<component>.image.repository`                                |                                                                                  | `zivgitlab.wwu.io/sciebo-rds/sciebo-rds/<component>` |
| `<component>.image.tag`                                       |                                                                                  | master                                               |
| `<component>.image.pullPolicy`                                |                                                                                  | Always                                               |
| `<component>.service.type`                                    |                                                                                  | ClusterIP                                            |
| `<component>.service.port`                                    |                                                                                  | 80                                                   |
| `<component>.service.targetPort`                              |                                                                                  | 8080                                                 |
| `<component>.service.annotations`                             |                                                                                  | prometheus.io/scrape: "true"                         |
| `<component>.resources.*`                                     | Set Limits and request resources                                                 | {}                                                   |
| `<component>.nodeSelector.*`                                  |                                                                                  | {}                                                   |
| `<component>.tolerations.*`                                   |                                                                                  | []                                                   |
| `<component>.affinity.*`                                      |                                                                                  | {}                                                   |
If you need more parameters, please take a look into the values.yaml of the corresponding service.

### Dependencies

This chart also use [jaeger](https://github.com/jaegertracing/helm-charts) and [redis-cluster](https://github.com/bitnami/charts/tree/master/bitnami/redis-cluster). Take a look to the corresponding repositories to find all options.

### Uninstall 

With the following command, you can remove the sciebo-rds system from your cluster.

```bash
helm uninstall sciebo-rds
```
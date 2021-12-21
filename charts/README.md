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

If you want to install the whole system, you can use the *all* chart, which depends on all services for sciebo RDS. You have to specify a values.yaml file to set all required parameters. The values.yaml should be taken from the getting-started folder here: https://github.com/Sciebo-RDS/getting-started/blob/master/deploy/values.yaml.example. Save this file as `values.yaml` in a directory of your choice. This file is your main configuration endpoint for sciebo RDS. So please change the content to your needs.

The following commands will add the needed repository, opens the `values.yaml` with vi and after you enter your credentials, it will try to install the chart with all services under the name "sciebo-rds" in your configured cluster with your `values.yaml`. If you changed something in the `values.yaml`, you only need to run the last command again.

```bash
helm repo add sciebo-rds https://www.research-data-services.org/charts/
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
---
sidebar_position: 3
id: kubernetes
displayed_sidebar: gettingstartedSidebar
---

# Configuring Kubernetes

## Requirements

- Access to a Kubernetes cluster (minikube, gcp, etc. - all are fine)
- Knowdledge of different services, like your Owncloud instance

We use [helm](https://helm.sh) to handle dependencies and configuration.

## Helm

1. Add our helm repository to your list.

```bash
$ helm repo add sciebords https://research-data-services.org/charts
```

---
2. Add the following `values.yaml` to a separate directory and edit it to your needs, especially the two domains for rds and describo.


```yaml
global:
  image:
    tag: v0.1.9 # set the same tag here as the same you used before for Owncloud
  namespace: # kubernetes separates applications in namespaces
    create: false # creates a namespace on its own
    name: "rds" # the name of the namespace, which will be used for sciebo RDS and / or created.
  describo: # all needed informations for describo
    api_secret: IAMSECRET # the api password, which is needed for all requests against the api
    domain: separate-domain-for-describo.your-institution.org # the domain you created for describo ui
  rds:
    domain: your-rds.institution.org # the domain you created for the sciebo rds ui
  # Domains you want to use as input, currently only owncloud supported,
  # this enables to use multiple owncloud instances with a single sciebo RDS
  domains:
    - name: owncloud.local # name needs to be exact the same as the second part after last @ in the cloudId
      ADDRESS: https://owncloud.local/owncloud # this has to be the exact owncloud domain 
      OAUTH_CLIENT_ID: ABC # given by the oauth plugin inside of owncloud
      OAUTH_CLIENT_SECRET: XYZ # given by the oauth plugin inside of owncloud
      SUPPORT_EMAIL: mail@side.com # a mail address you want to show to the users in multiple places inside of the ui
      MANUAL_URL: usermanual.side.com # an url to a manual you want to show to the users in ui
layer0-describo: # describo`s specific options
  postgresql: # starts its own postgresql database.
    postgresqlDatabase: "describo"
    postgresqlUsername: "admin"
    postgresqlPassword: "admin"
layer0-web: # sciebo rds UI specific options
  environment: # env vars given into the container
    SECRET_KEY: 1234 # the password, which will be used to encrypt all user data
layer1-port-zenodo: # zenodo`s specific options
  enabled: true # here you could disable it, but who would like to do it?
  environment: # needs to be adjusted to correct values
    ADDRESS: https://sandbox.zenodo.org # the testing instance
    # ADDRESS: https://zenodo.org # the main instance of zenodo.
    OAUTH_CLIENT_ID: ABC # given by the OAUTH process of the used zenodo instance from above.
    OAUTH_CLIENT_SECRET: XYZ # given by the OAUTH process of the used zenodo instance from above.
```

The file can also be found here: [values.yaml](https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/develop/getting-started/values.yaml).

---
3. Apply the `values.yaml` configuration to your cluster:

```bash
$ helm upgrade -i sciebords -f values.yaml sciebords/all
```

---

This is it. Sciebo RDS is now ready to use through the Owncloud plugin. 
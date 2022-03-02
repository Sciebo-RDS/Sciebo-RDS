---
title: "Kubernetes"
subtitle: "Requirements, Configuration and Helm Charts"
weight: 300

menu:
  doc:
    parent: installation 
---

In the following, we will show you how to install the RDS system in your Kubernetes Cluster.

{{<callout "info">}} If you do not already know, what RDS is and how does it work, you should take a look into
this [article](/doc/). {{</callout>}}

At the beginning of this guide, you will need to fulfill the requirements. After that, you will need to configure the
RDS system to your needs. Last but not least, you will install the RDS system on your configured kubernetes cluster.

{{<callout "info">}} In earlier versions of this document, we used make(-file). This has been replaced in favor of more transparent `helm` commands. They are compatible with the commands in the makefile, so you do not have to replace your current setup. But the helm charts were updated by alot. So you should use `helm repo update` and `helm upgrade` command [we use later in this document](#installation) to get to the latest version.
{{</callout>}}

## Assumptions

Every RDS system is:

- not publicly available on the Internet, but only through one of the plugins described in this documentation.
- only made publicly available by a single plugin.
- not trimmed for throughput.

## Requirements

The version control program used is [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

Furthermore
a [Kubernetes](https://kubernetes.io/docs/home/) ([local installation via Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/)
, Windows WSL2
Integration[[1]](https://kubernetes.io/blog/2020/05/21/wsl-docker-kubernetes-on-the-windows-desktop/)[[2]](https://kubernetes.io/blog/2020/05/21/wsl-docker-kubernetes-on-the-windows-desktop/#minikube-kubernetes-from-everywhere))
cluster is required, which offers
a [Docker-compatible Runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)

The [user account](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) must have the following rights:

- Creation of own deployments
- Generation of own secrets
- Creation of own ConfigMaps
- Creation of own DaemonSets
- Generation of own services

These rights are rather fundamental for working with Kubernetes and should be available for every user account. However,
in some environments, it may be necessary to contact the cluster administrator about these rights and obtain appropriate
permissions.

The following rights are optional, but highly recommended:

- creation of Namespaces (Also can be done through your cluster administtrator)

{{<callout "info">}} Use `minikube` for test purposes, otherwise ask the cluster administrator for access informations.
{{</callout>}}

The provided scripts uses *nano* to open files. Please be sure to installed it.

### Ingress

The system needs an ingress server. If you want to use `minikube`, you can add it with the following command. Otherwise,
please ask your Kubernetes cluster administrator.

```bash
minikube addons enable ingress
```

### Required programs

You need the following tools installed and configured:

- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [helm](https://helm.sh/docs/intro/install/)
- vim (or any other text editor like nano)
- unzip

{{<callout "tip">}} Note: Since Helm v3 no Tillerserver is [required](https://helm.sh/blog/helm-3-released/) on the
Kubernetes side. {{</callout>}}

## Configuration

You need a `values.yaml` to configure sciebo RDS. [An example file can be found here](https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/release/getting-started/values.yaml.example).
Please copy and paste the content of the linked file into a file named `values.yaml` in a place, which you can remember nicely.

Each service that will be used by the RDS system may be adjusted with respect to local needs. If you are
fine with the standard values, you do not need any changes for your services except connector-services. But if you want
to change any value, you need to specify it in the `values.yaml` for the corresponding microservice. If you want to see
every available parameter, please take a look at
the [chart repo](https://github.com/Sciebo-RDS/Sciebo-RDS/tree/release/charts).

For the connector-services, you need to specify the OAuth-ID and -secret to identify with. If you take a look into your `values.yaml` file, you will find multiple oauth id and secret
environment variables. This needs to be set up to work correctly with the corresponding services, which will be
connected. In the following section [Generate OAuth2 Identifier and Secrets](#generate-oauth2-identifier-and-secrets)
you will find out how.

You have to set `enabled: true` for each service, you want to use. Only for enabled services, you need to set the oauth
values. Once these adjustments have been made, the system can be installed. Some services can be disabled too (like the `layer0-web` service), but if you do not know what you are doing, you should not do that. So only touch services in layer1.

In the `values.yaml` you will find an object named `describo`. This is a tool for metadata collection. Please adjust it according to its [manual](https://github.com/Arkisto-Platform/describo-online/wiki/General-information-about-configuring-the-application).

If you want to use sciebo RDS for multiple EFSS you have to configure the `global.domains` object within `values.yaml`. For more informations, please take a look at the next chapter.

### Multiple EFSS with a single sciebo RDS installation

{{<callout info>}} Currently this approach only applies to ownCloud EFSS installation only. Other EFSS are not supported right now. {{</callout>}}

For this purpose we develop a tool to help: [Sciebo RDS CLI](https://github.com/Sciebo-RDS/Sciebo-RDS-CLI). Please follow the installation steps. Otherwise you need to configure the `global.domains` object on your own. An example can be found in [values.yaml.example](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/develop/getting-started/values.yaml.example). You have to remove this object, if you want to only serve a single installation. Please remove the `domains` object, because it overwrites your `layer1-port-owncloud` configuration otherwise. But you can use it for a single installation, too. (Maybe you want to add later other instances) Then you do not need to fill out the informations in `layer1-port-owncloud`. Also it overwrites all other ports which will be used as filestorage within sciebo RDS e.g. `layer1-port-reva` etc., so you cannot use reva and multiple ownCloud-instances at once. Please use separate sciebo RDS instances for this use-case.

### Generate OAuth2 identifier and secrets

You have to generate the oauth credentials for your used oauth2 service provider. This credentials are generated, when
you create an oauth application. The following table redirects you to the corresponding websites.

{{<callout info>}} The following assumes that your owncloud installation is available under `owncloud.local`. Adjust
this to your needs. {{</callout>}}

| Service                | oauth application creation url                                             |
| ---------------------- | -------------------------------------------------------------------------- |
| Zenodo                 | https://`(sandbox.)`zenodo.org/account/settings/applications/              |
| ownCloud               | https://`owncloud.local`/index.php/settings/admin?sectionid=authentication |
| Open Science Framework | https://`(test.)`osf.io/settings/applications                              |

The application creation requires an `redirect url`. This needs to be adjusted to your used plugin, which integrates
your RDS instance into client user interfaces. The following endpoint needs to be used for your installation, when you
use the given plugin.

{{<callout info>}} Please remember the name, which you give your application in your owncloud installation, because you
need this name in the configuration of the owncloud plugin. {{</callout>}}

| plugin   | oauth endpoint | example endpoint                              |
| -------- | -------------- | --------------------------------------------- |
| ownCloud | /              | https://`your-cluster-domain-for-sciebo-rds`/ |

This url must also be configured in your `configuration.yaml` under the environment variable `RDS_OAUTH_REDIRECT_URI`,
since this information must be set for each request to your oauth2 service providers.

{{<callout info>}} Multiple oauth2 service providers requires a `https` connection. {{</callout>}}

After this, you have the informations to fill out the `values.yaml` file.

### Namespace

It is recommended to create a
separate [namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) for RDS in
Kubernetes (e.g. named *research-data-services*). The helm charts can do that for you. Open up the `values.yaml` and configure the following line in root layer to your needs:

If you want to create a namespace, rename the file "namespace.yaml.example" to "namespace.yaml" and apply it. You can
use the following commands to do this.

{{<tabs>}} {{<tab "yaml" "Apply namespace">}}namespace:
  create: true
  name: "research-data-services"
{{</tab>}}

{{<tab "yaml" "Remove namespace">}}namespace:
  create: false
  name: "research-data-services"
{{</tab>}} {{</tabs>}}

So if the namespace is not existing, it creates it. With this configuration, `helm` will remove the namespace when you remove sciebo RDS from your cluster, too. The `name` parameter configures the name of the namespace.

### Helm Repo

We use helm charts (we said it earlier in this documentation). So you have to add the repository to your helm list.

{{<tabs>}}
{{<tab "bash" "Add helm charts">}}helm repo add sciebo-rds https://www.research-data-services.org/charts/stable/index.yaml
helm repo update
{{</tab>}}
{{<tab "bash" "Remove helm charts">}}helm repo remove sciebo-rds
{{</tab>}}
{{</tabs>}}

### Encryption

If the communication between plugins and cluster shall be secured by a HTTPS connection, which is strongly recommended,
you can create a certificate using the shell
script [create_certs.sh](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/develop/getting-started/create_certs.sh.example) and store it
as a secret. The script has to be adapted regarding the domain, for which the certificate shall be issued.
Please download the script into a file named `create_certs.sh` a place where you can find it later. Adjust it to your needs.

With the following command, you can create the needed ssl cert.

{{<tabs>}} {{<tab "bash" "Create and apply ssl cert">}}chmod +x create_certs.sh && ./create_certs.sh {{</tab>}}

{{<tab "bash" "Delete ssl cert">}}kubectl delete secret $(sed -n 's/CERT_NAME=\(.*\)/\1/p' < create_certs.sh) {{</tab>}} {{</tabs>}}

{{<callout info>}} If you want to use an already existing certificate, please store it as secret in the RDS namespace
with the name `sciebords-tls-public`. See the shell script `create_certs.sh` for an example. If you want to change the
secret name, you need to set the name in your `values.yaml` under `global.ingress.tls.secretName` and restart the
system. {{</callout>}}

## Installation

{{<callout "warning">}} The commands in this chapter needs some configuration, which you made in the previous chapter.
If you did not create the needed files, you will get a lot of error messages now. So please be sure to follow the steps
from the [configuration tutorial](/doc/getting-started/k8s/#configuration). {{</callout>}}

Now the RDS ecosystem can be loaded onto the cluster with the following command:

{{<tabs>}} {{<tab "bash" "Install RDS">}}helm upgrade sciebo-rds sciebo-rds/all -i --values values.yaml {{</tab>}}

{{<tab "bash" "Uninstall RDS">}}helm uninstall sciebo-rds {{</tab>}} {{</tabs>}}

### Monitoring

The system automatically installs a Jaeger instance for tracking log messages. You can access this instance with the
following command and then call up the displayed IP address in the browser:

```bash
$(eval POD_JAEGER=$(shell kubectl get pods -l "app.kubernetes.io/name=jaeger,app.kubernetes.io/component=query" -o jsonpath="{.items[0].metadata.name}")) 
echo http://127.0.0.1:8080/
kubectl port-forward $(POD_JAEGER) 8080:16686
```

Jaeger is particularly well suited for identifying errors or problems within the ecosystem.

If a Prometheus system is used, all metrics are automatically tapped and offered in the respective system. A
standardised view will be offered in the future (see [Issue 39](https://github.com/Sciebo-RDS/Sciebo-RDS/issues/39)).

### Access to your RDS installation

If you do not have a NIC-System to manage a domain and use minikube as your cluster installation, you should configure
your local hosts-file to redirect a domainlookup-request to your `localhost`. With the following command, you can
configure this. It assumed, that the local domain, which was configured previously, was `rds.local`. If you changed it
in the configuration process, you have to change it here approparly.

{{<tabs>}} {{<tab "bash" "Linux">}}export RDS_DOMAIN=rds.local echo "$(minikube ip) $RDS_DOMAIN" | sudo tee -a /etc/hosts {{</tab>}}

{{<tab "bash" "Windows">}}minikube.exe ip # remember that
# we open Notepad for you with admin priviliges and you have to append the following to the file
# <minikube-ip> rds.local
start -verb runas notepad.exe C:\Windows\system32\drivers\etc\hosts {{</tab>}} {{</tabs>}}

Now you can open your browser and enter `https://rds.local/port-service/service`. Now you should see a list with some
JWT-encoded entries. If you decode them, you will find out, that this holds your configuration about your
oauth2-services within RDS.

## Finish the installation

Since the server-side installation of the RDS instace has now been completed, a client plugin is required. Currently the
following plugins are available:

- [ownCloud Plugin](/doc/impl/plugins/owncloud/)
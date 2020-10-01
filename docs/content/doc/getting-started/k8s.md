---
title: Kubernetes
subtitle: Requirements, Configuration and Helm Charts

menu:
  doc:
    parent: installation
weight: 300
---

In the following, we will show you how to install the RDS system in your Kubernetes Cluster.

{{<callout "info">}}
If you not already know, what RDS is and how does it work, you should take a look into this [article](/doc/).
{{</callout>}}

At the beginning of this guide, you will need to fulfill the requirements. After that, you will need to configure the RDS system to your needs. Last but not least, you will install the RDS system on your configured kubernetes cluster.

## Assumptions

Every RDS system is:

- not publicly available on the Internet, but only through one of the plugins described in this documentation.
- only made publicly available by a single plugin.
- not trimmed for throughput.

## Requirements

The version control program used is [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

Furthermore a [Kubernetes](https://kubernetes.io/docs/home/) ([local installation via Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/), Windows WSL2 Integration[[1]](https://kubernetes.io/blog/2020/05/21/wsl-docker-kubernetes-on-the-windows-desktop/)[[2]](https://kubernetes.io/blog/2020/05/21/wsl-docker-kubernetes-on-the-windows-desktop/#minikube-kubernetes-from-everywhere)) cluster is required, which offers a [Docker-compatible Runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)

The [user account](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) must have the following rights:
- Creation of own deployments
- Generation of own secrets
- Creation of own ConfigMaps
- Creation of own DaemonSets
- Generation of own services

These rights are rather fundamental for working with Kubernetes and should be available for every user account. However, in some environments, it may be necessary to contact the cluster administrator about these rights and obtain appropriate permissions.

The following rights are optional, but highly recommended:
- creation of Namespaces

{{<callout "info">}}
Use `minikube` for test purposes, otherwise ask the cluster administrator for access informations.
{{</callout>}}

The provided scripts uses *nano* to open files. Please be sure to installed it.

### Ingress

The system needs an ingress server. If you want to use `minikube`, you can add it with the following command. Otherwise, please ask your Kubernetes cluster administrator.

```bash
minikube addons enable ingress
```

### Required programs

We use the program `make` to configure and deploy our software with a Makefile, which can be found in the `deploy` folder. If `helm` or `kubectl` have not yet been installed, you can easily install them with the following commands, too.

{{<tabs>}}
{{<tab "bash" "Ubuntu/Debian">}}sudo apt install make -y
make dependencies_ubuntu
{{</tab>}}

{{<tab "bash" "Fedora/CentOS">}}sudo dnf install make -y
make dependencies_fedora
{{</tab>}}

{{<tab "bash" "Windows 10 Powershell">}}Set-ExecutionPolicy AllSigned
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco install -y make
make dependencies_windows
# You cannot use all commands in the following, please translate from linux to windows commands by yourself.
{{</tab>}}
{{</tabs>}}

{{<callout "tip">}}
Note: Since Helm v3 no Tillerserver is [required](https://helm.sh/blog/helm-3-released/) on the Kubernetes side.
{{</callout>}}

## Configuration

You need the folder `deploy` from the Github repository.

```bash
git clone https://github.com/Sciebo-RDS/Sciebo-RDS.git
cd ScieboRDS/deploy
```

It contains all the files which are required for configuration and installation.

{{<callout info>}}
If you want to see the helm charts, take a look at the [charts repo](https://github.com/Sciebo-RDS/charts).
{{</callout>}}

To customize the installation, several files have to be adjusted. For this purpose, there are `.example` files in the `deploy` folder which needs to be copied, renamed and adapted as necessary.

```bash
cp configuration.yaml.example configuration.yaml
nano configuration.yaml
```

In `configuration.yaml` the proxies that may be necessary in the environment are to be defined. This allows the microservices to reach services available outside of the cluster, if the cluster does not have its own global IP. You might want to ask your local network administrator concerning the correct proxy configuration for your environment.

Furthermore, each service that will be used by the RDS system may be adjusted with respect to local needs. If you are fine with the standard values, you do not need any changes for your services except connector-services. But if you want to change any value, you need to specify it in the `values.yaml` for the corresponding microservice. If you want to see every available parameter, please take a look at the [chart repo](https://github.com/Sciebo-RDS/charts/tree/master/charts).

For the connector-services, you need to specify the OAuth-ID and -secret to identify with.
There are again an `example` file to be found in the `deploy` folder, which is called `values.yaml.example`. This file have to be renamed following the pattern laid out above, i.e. pruning the respective example suffix. You may also change the corresponding data for the services if necessary.

```bash
cp values.yaml.example values.yaml
nano values.yaml
```

{{<callout info>}}
If you take a look into your `values.yaml` file, you will find multiple oauth id and secret environment variables. This needs to be set up to work correctly with the corresponding services, which will be connected. In the following section [Generate OAuth2 Identifier and Secrets](#generate-oauth2-identifier-and-secrets) you will find out how.
{{</callout>}}

Once these adjustments have been made, the system can be installed.

### Generate OAuth2 identifier and secrets

You have to generate the oauth credentials for your used oauth2 service provider. This credentials are generated, when you create an oauth application. The following table redirects you to the corresponding websites.

{{<callout info>}}
The following assumes that your owncloud installation is available under `owncloud.local`. Adjust this to your needs.
{{</callout>}}

| Service  | oauth application creation url                                           |
| -------- | ------------------------------------------------------------------------ |
| Zenodo   | https://(sandbox.)zenodo.org/account/settings/applications/              |
| ownCloud | https://`owncloud.local`/index.php/settings/admin?sectionid=authentication |

The application creation requires an `redirect url`. This needs to be adjusted to your used plugin, which integrates your RDS instance into client user interfaces. The following endpoint needs to be used for your installation, when you use the given plugin.

{{<callout info>}}
Please remember the name, which you give your application in your owncloud installation, because you need this name in the configuration of the owncloud plugin.
{{</callout>}}

| plugin   | oauth endpoint           | example endpoint                                  |
| -------- | ------------------------ | ------------------------------------------------- |
| ownCloud | index.php/apps/rds/oauth | https://`owncloud.local`/index.php/apps/rds/oauth |

This url must also be configured in your `configuration.yaml` under the environment variable `RDS_OAUTH_REDIRECT_URI`, since this information must be set for each request to your oauth2 service providers.

{{<callout info>}}
Multiple oauth2 service providers requires a `https` connection.
{{</callout>}}

After this, you have the informations to fill out the `values.yaml` file.

### Namespace

It is recommended to create a separate [namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) for RDS in Kubernetes (e.g. named *research-data-services*).

{{<callout warning>}}
If you do not follow the commands in this section, all commands must be completed respectively and the tools provided in what follows cannot be used straightforwardly. So you need to adjust all commands in the makefile to your needs or execute them manually and at your chosen namespace per hand.
{{</callout>}}

If you want to create a namespace, rename the file "namespace.yaml.example" to "namespace.yaml" and apply it. You can use the following commands to do this.

{{<tabs>}}
{{<tab "bash" "Apply namespace">}}cp namespace.yaml.example namespace.yaml
nano namespace.yaml
make install_namespace
kubectl config set-context --current --namespace=$(grep 'name:' namespace.yaml | tail -n1 | awk '{ print $2}')
{{</tab>}}

{{<tab "bash" "Remove namespace">}}kubectl config set-context --current --namespace=default
make uninstall_namespace
{{</tab>}}
{{</tabs>}}

After the last command, specifying a context for each Kubectl command (the same with helm) becomes obsolete because the specified namespace is used as a default. 

### Encryption

If the communication between plugins and cluster shall be secured by a HTTPS connection, which is strongly recommended, you can create a certificate using the shell script [create_certs.sh](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/master/deploy/create_certs.sh) and store it as a secret. The script has to be adapted regarding the domain, for which the certificate shall be issued.

With the following command, you can create the needed ssl cert.

{{<tabs>}}
{{<tab "bash" "Create and apply ssl cert">}}cp create_certs.sh.example create_certs.sh
nano create_certs.sh
make install_tls
{{</tab>}}

{{<tab "bash" "Delete ssl cert">}}make uninstall_tls
{{</tab>}}
{{</tabs>}}

{{<callout info>}}
If you want to use an already existing certificate, please store it as secret in the RDS namespace with the name `sciebords-tls-public`. See the shell script `create_certs.sh` for an example.
If you want to change the secret name, you need to set the name in your `values.yaml` under `global.ingress.tls.secretName` and restart the system.
{{</callout>}}

### Apply the configuration

If you follow the previous steps, you can now apply the configuration to your kubernetes cluster.

{{<tabs>}}
{{<tab "bash" "Apply configuration">}}make install_configuration
{{</tab>}}

{{<tab "bash" "Undoing configuration">}}make uninstall_configuration
{{</tab>}}
{{</tabs>}}


## Installation

{{<callout "warning">}}
The commands in this chapter needs some configuration, which you made in the previous chapter. If you did not create the needed files, you will get a lot of error messages now. So please be sure to follow the steps from the [configuration tutorial](/doc/getting-started/config/).
{{</callout>}}

Now the RDS ecosystem can be loaded onto the cluster with the following command:

{{<tabs>}}
{{<tab "bash" "Install RDS">}}make install
{{</tab>}}

{{<tab "bash" "Uninstall RDS">}}make uninstall
{{</tab>}}
{{</tabs>}}

### Monitoring

The system automatically installs a Jaeger instance for tracking log messages. You can access this instance with the following command and then call up the displayed IP address in the browser:

```bash
make jaeger
```

Jaeger is particularly well suited for identifying errors or problems within the ecosystem.

If a Prometheus system is used, all metrics are automatically tapped and offered in the respective system. A standardised view will be offered in the future (see [Issue 39](https://github.com/Sciebo-RDS/Sciebo-RDS/issues/39)).

### Access to your RDS installation

If you do not have a NIC-System to manage a domain and use minikube as your cluster installation, you should configure your local hosts-file to redirect a domainlookup-request to your `localhost`. With the following command, you can configure this. It assumed, that the local domain, which was configured previously, was `rds.local`. If you changed it in the configuration process, you have to change it here approparly.

{{<tabs>}}
{{<tab "bash" "Linux">}}export RDS_DOMAIN=rds.local
echo "$(minikube ip) $RDS_DOMAIN" | sudo tee -a /etc/hosts
{{</tab>}}

{{<tab "bash" "Windows">}}minikube.exe ip # remember that
# we open Notepad for you with admin priviliges and you have to append the following to the file
# <minikube-ip> rds.local
start -verb runas notepad.exe C:\Windows\system32\drivers\etc\hosts
{{</tab>}}
{{</tabs>}}

Now you can open your browser and enter `https://rds.local/port-service/service`. Now you should see a list with some JWT-encoded entries. If you decode them, you will find out, that this holds your configuration about your oauth2-services within RDS.

## Finish the installation

Since the server-side installation of the RDS instace has now been completed, a client plugin is required. Currently the following plugins are available:

- [ownCloud Plugin](/doc/impl/plugins/owncloud/)
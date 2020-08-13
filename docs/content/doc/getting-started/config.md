---
title: Configuration
subtitle: Where you configure the installation

menu:
  doc:
    parent: installation
weight: 301
---


You need the folder `deploy` from the Github repository.

```bash
git clone https://github.com/Sciebo-RDS/Sciebo-RDS.git
cd ScieboRDS/deploy
```

It contains all the files which are required for configuration and installation.

{{<callout info>}}
If you want to see the helm charts, take a look at the [charts repo](https://github.com/Sciebo-RDS/charts).
{{</callout>}}

## Configuration

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

Once these adjustments have been made, the system can be installed.

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
kubectl config set-context --current --namespace=$(sed -n 's/name: \(.*\)/\1/p' < namespace.yaml | head -n 1)
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
{{<tab "bash" "Create and apply ssl cert">}}cp create_cert.sh.example create_cert.sh
nano create_cert.sh
make install_tls
{{</tab>}}

{{<tab "bash" "Delete ssl cert">}}make uninstall_tls
{{</tab>}}
{{</tabs>}}

{{<callout info>}}
If you want to use an already existing certificate, please store it as secret in the RDS namespace with the name `sciebords-tls-public`. See the shell script `create_cert.sh` for an example.
If you want to change the secret name, you need to set the name in your `values.yaml` under `global.ingress.tls.secretName` and restart the system.
{{</callout>}}

## Apply the configuration

If you follow the previous steps, you can now apply the configuration to your kubernetes cluster.

{{<tabs>}}
{{<tab "bash" "Apply configuration">}}make install_configuration
{{</tab>}}

{{<tab "bash" "Undoing configuration">}}make uninstall_configuration
{{</tab>}}
{{</tabs>}}

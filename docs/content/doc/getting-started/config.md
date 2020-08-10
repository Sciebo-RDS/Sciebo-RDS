---
title: Configuration
subtitle: Where you configure the installation

menu:
  doc:
    parent: installation
weight: 301
---


You need the folder "deploy" from the Github repository.

```bash
git clone https://github.com/Sciebo-RDS/Sciebo-RDS.git
cd ScieboRDS/deploy
```

It contains all the files which are required for configuration and installation.

{{<callout info>}}
If you only want to install via helm charts, you can use the following command to add our helm chart repository:

```bash
helm repo add sciebo-rds https://sciebo-rds.github.io/charts/
```
{{</callout>}}

To customize the installation, several files have to be adjusted. For this purpose, there are ".example" files in the deployment and in all the respective microservice folders, which are to be copied, renamed and adapted as necessary.

```bash
cp kustomization.yaml.example kustomization.yaml
nano kustomization.yaml
```

In kustomization.yaml the proxies that may be necessary in the environment are to be defined. This allows the microservices to reach services available outside of the cluster, if the cluster does not have its own global IP. You might want to ask your local network administrator concerning the correct proxy configuration for your environment. 

Furthermore, each service that will be used by the RDS system may be adjusted with respect to local needs, thereby ensuring that the system actually sets up exactly the services that are needed as appropriate.

There are again "example" files to be found in the folders of all the different services, which are called "values.yaml.example". They have to be renamed following the pattern laid out above, i.e. pruning the respective example suffixes. You may also change the corresponding data for the services if necessary.

```bash
cp values.yaml.example values.yaml
nano values.yaml
```

Once these adjustments have been made, the cluster can be installed.

If the communication between plugins and cluster shall be secured by a HTTPS connection, which is strongly recommended, you can create a certificate using the shell script [create_certs.sh](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/master/deploy/create_certs.sh) and store it as a secret. The script has to be adapted regarding the domain, for which the certificate shall be issued.

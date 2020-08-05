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

It contains all files which are required for configuration and installation.

To customize the installation, several files have to be adjusted. For this purpose, there are ".example" files in the deployment and in the respective microservice folders, which are to be copied and renamed and then adapted.

```bash
cp customization.yaml.example customization.yaml
nano customization.yaml
```

In kustomization.yaml the proxies that may be necessary in the environment are defined. This allows the microservices to reach services available outside the cluster if the cluster does not have its own global IP.

Each service that is to be used requires the following adaptation. This ensures that the system actually sets up the services that the user wants to use.

In the folders of the different services there are again "example" files, more precisely "values.yaml.example", which must be renamed as above. In these files you now have to enter the corresponding data for the services.

```bash
cp values.yaml.example values.yaml
nano values.yaml
```

Once these adjustments have been made, the cluster can now be installed.

If the communication between plugins and cluster should be secured by a HTTPS connection, which is strongly recommended, you can create a certificate with the shell script [create_certs.sh](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/master/deploy/create_certs.sh) and store it as a secret. The script has to be adapted for which domain the certificate should be issued.

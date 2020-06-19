---
title: Configuration
subtitle: Where you configure the installation

menu:
  doc:
    parent: installation
weight: 301
---


The folder again contains "example" files, more precisely "values.yaml.example", which must be renamed as above. In these files you now have to enter the corresponding data for the services.

``bash
cp values.yaml.example values.yaml
nano values.yaml
```

Once these adjustments have been made, the cluster can now be installed.

If the communication between plugins and cluster should be secured by a HTTPS connection, which is strongly recommended, you can create a certificate with the shell script [create_create.sh](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/master/deploy/create_certs.sh) and store it as a secret. The script has to be adapted for which domain the certificate should be issued.

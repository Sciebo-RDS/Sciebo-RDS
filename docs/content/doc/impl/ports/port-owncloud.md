---
title: Port Owncloud
subtitle: Work on your files from owncloud within RDS

menu:
  doc:
    parent: adapter-port
weight: 600
---

# Mission

This service handles all communication with the configured Owncloud instance and makes its files available to the RDS system.

Currently, this service can only be used as a source service for the configuration of research projects, since currently only the download of files is implemented.

## OpenAPI v3

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/layer2_use_cases/interface_port_file_storage.yml" >}}

## Implementation

The following class implements a library to use an owncloud installation.

{{% code file="doc/impl/ports/port-owncloud-docstring.md" %}}

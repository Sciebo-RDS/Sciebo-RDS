---
title: Path definitions
subtitle: Where to find the services

menu:
  doc:
    parent: infrastructure
mermaid: true
weight: 500
---

## Domain

The domain is defined in the central configuration file, [as described here](/doc/getting-started/config/). The following definitions are specified as folders under this domain. If your domain is `example.com', then an example service `folder' can be found as follows: `example.com/folder' .

## Path definitions

The following path definitions are defined by the respective services and can therefore be accessed from outside.

| Service          | Path definition |
| ---------------- | --------------- |
| Port Service     | /port-service   |
| Exporter Service | /exporter       |
| Metadata Service | /metadata       |

The service-specific subfolders and endpoints are defined in the respective OpenAPI file and can be viewed in this documentation.

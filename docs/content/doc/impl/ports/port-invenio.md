---
title: Port Zenodo
subtitle: Export your package to a Zenodo repository.

menu:
  doc:
    parent: adapter-port
weight: 601
---

# Mission

This service handles all communication with the configured Owncloud instance and makes its files available to the RDS system.

When creating research projects, this service can be configured as source and target service.

## OpenAPI v3

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle2_use_cases/interface_port_metadata.yml" >}}

## Implementation

The following class implements a library to use the Invenio installation "Zenodo".

{{% code file="doc/impl/ports/port-invenio-docstring.md" %}}

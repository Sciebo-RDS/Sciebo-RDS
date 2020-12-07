---
title: Port OpenScienceFramework
subtitle: Export your package to a OpenScienceFramework repository.

menu:
  doc:
    parent: adapter-port
weight: 601
---

# Mission

This service handles all communication with the configured OpenScienceFramework address and makes its files available to the RDS system.

When creating research projects, this service can be configured as source and target service.

## OpenAPI v3

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/informations-ep/RDS/circle2_use_cases/interface_port_metadata.yml" >}}

## Implementation

{{% code file="doc/impl/ports/port-osf-docstring.md" %}}

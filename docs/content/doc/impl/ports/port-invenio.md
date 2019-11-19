---
title: Port Zenodo
subtitle: Export your package to an invenio repository.

menu:
  doc:
    parent: adapter-port
weight: 1000
---

# OpenAPI v3

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/port_zenodo-service/RDS/circle2_use_cases/port_invenio.yml"  >}}

# Implementation

The following classes implements a library to work easier with zenodo in the zenodo service.

{{% code file="doc/impl/ports/port-invenio-docstring.md" %}}

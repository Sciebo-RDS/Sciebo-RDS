---
title: Port Invenio
subtitle: Export your package to an invenio repository.

menu:
  doc:
    parent: adapter-port
weight: 1000
---

## OpenAPI v3

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle2_use_cases/port_invenio.yml"  >}}

## Implementierung

Die folgende Klasse implementiert eine Bibliothek, um die Invenio-Installation "Zenodo" verwenden zu können.

{{% code file="doc/impl/ports/port-invenio-docstring.md" %}}

---
title: Exporter Service
subtitle: Für das Exportieren und Importieren von Daten durch die Ports

menu:
  doc:
    parent: use-case
weight: 701
mermaid: True
---

# Mission

The Exporter Service ensures that the integration plugin only needs to call a few end points and that many different functionalities are only available to the RDS system. This ensures that no information is available to the outside world as long as authentication by the plugin is ensured.

The export of files is done based on previously set research projects in the Research Manager.

The service can also be used as importer by swapping the export services in the corresponding research project (as long as the service supports this).

## OpenAPI

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/layer2_use_cases/exporter/use-case_exporter.yml" >}}

{{% code file="doc/impl/use-cases/exporter-service-docstring.md" %}}

---
title: Metadata Service
subtitle: Für die Verbindung und Erhalt der Metadaten aus den Ports.

menu:
  doc:
    parent: use-case
weight: 702
mermaid: True
---

# Mission

The Metadata Service ensures that the integration plugin only needs to call a few endpoints and that many different functionalities are only available to the RDS system. This ensures that no information is available to the outside world as long as authentication by the plugin is ensured.

This service provides functions for viewing and editing metadata for files and research projects. It handles all requests to the corresponding ports, so that the plugin only needs to call one endpoint and all further calls are triggered RDS-internally based on the stored research project.

## OpenAPI

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle2_use_cases/metadata/use-case_metadata.yml" >}}

{{% code file="doc/impl/use-cases/metadata-service-docstring.md" %}}

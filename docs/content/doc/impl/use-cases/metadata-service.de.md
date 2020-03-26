---
title: Metadata Service
subtitle: Alle metadata-relevanten Informationen können hier abgerufen und gespeichert werden.

menu:
  doc:
    parent: use-case
weight: 1001
---

# Einführung

Dieser Dienst ist darin besonders, dass er selbst keine Informationen abspeichert, sondern eine zentrale Anlaufstelle für alle Metadaten darstellt. Der Service propagiert dann die erhaltenen Metadaten an die entsprechenden Ports weiter, sodass sich der Entwickler einer Anwendung darum nicht kümmern muss. Dafür wird intern das DataCite [Datenmodell](https://github.com/datacite/schema/tree/master/source/json/kernel-4.3/example) verwendet, sodass die Ports dieses auch verstehen müssen und es entsprechend des angebunden Services übersetzen müssen. Dafür definiert dieser Metadaten Service eine Schnittstellen-API für die [Port-APIs](https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle2_use_cases/port_metadata.yml), welche als Metadatenspeicher verwendet werden soll, sodass dieser Service über die Ports mit den angeschlossenen Services kommunizieren kann.

## Sequence Diagram

TODO: Make a mermaid diagram, which describes the sequence to update and get all metadata. 

# OpenAPI v3

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle2_use_cases/metadata/use-case_metadata.yml" >}}

{{% code file="doc/impl/use-cases/metadata-service-docstring.md" %}}

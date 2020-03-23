---
title: Projekt Manager
subtitle: Alle Projekte in RDS

menu:
  doc:
    parent: core
weight: 1101
mermaid: true
---

# Einführung

Dieser Service stellt einen projektbasierten Informationsspeicher dar, sodass alle anderen Microservices sich auf diese berufen können. Hier wird u.a. festgestellt, welche Ports verwendet werden sollen beim Veröffentlichen von Daten.


## ER-Diagramm

Das interne Informationsmodell wird im folgenden als UML-Diagramm dargestellt, soll aber bitte als ER-Diagramm verstanden werden.

```mermaid
classDiagram

  class Port {
    - String portName
    - Bool fileStorage
    - Bool metadataStorage
    - Dict customProperty
  }

  class Project {
    + String user
    + Port portIn
    + Port portOut
  }

  class ProjectService {
    + Project projects
  }

  ProjectService "1" -- "0..n" Project : has
  Project "1" -- "0..n" Port : has
```

# OpenAPI v3

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle3_central_services/project_manager/central-service_project-manager.yml"  >}}

{{% code file="doc/impl/central/project-manager-docstring.md" %}}

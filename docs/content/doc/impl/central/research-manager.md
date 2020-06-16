---
title: Research Manager
subtitle: All studies in RDS

menu:
  doc:
    parent: core
weight: 1101
mermaid: true
---

# Introduction

This service represents the project based storage, so the user can store his service projects in the rds system.

## Explanation of the term research project

Due to the very high frequency of the term *project* in computer science and associated services, we had to choose a different term within the RDS system to simplify communication between users and/or developers. That's why we chose the term research project to refer to projects within the RDS system, which can be loosely translated into English as *Research*, in order to always be able to distinguish which project is meant in the dialog: either the research project in the RDS system or the project of an associated service. It also increases readability and makes the meaning of terms within this documentation and the RDS implementation much clearer.

For example, it is clear which ID is involved if the API endpoint requires a *research-id* (rds internal project identifier) or a *project-id* (service-specific project identifier). Which *project-id* it is depends on the context, e.g. the port of the Zenodo service often requires a *project-id*, which is assigned specifically for Zenodo.


## ER Diagram

The internal information model is presented in the following as a UML diagram, but should please be understood as an ER diagram.

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

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle3_central_services/research_manager/central-service_research-manager.yml"  >}}

{{% code file="doc/impl/central/research-manager-docstring.md" %}}

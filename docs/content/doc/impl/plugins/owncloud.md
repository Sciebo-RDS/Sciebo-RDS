---
title: OwnCloud
subtitle: How to use RDS with OwnCloud

menu:
  doc:
    parent: plugins
weight: 900
mermaid: true
---


This plugin represents the first integration of RDS into another ecosystem. In order to ensure usability and to keep the threshold as low as possible, care is taken to use as many functionalities of the platform as possible and to extend them by RDS.

## Settings

In the settings, the user has the option of storing OAuth tokens and passwords (which are also referred to as tokens in the following) in the system, with which the system can log on to various services on behalf of the user. The following status diagram illustrates the process.

### Input masks of the settings

``mermaid
stateDiagram
  [*] --> Start
  Start --> RDS: no
  Start --> Z: yes
  Z --> Zenodo: no
  Z --> [*]: yes

  RDS --> Start
  Zenodo --> Start

  Start: RDS activated?
  Z: Zenodo activated?

  state RDS {
    [*] --> A
    A --> B: Button pressed
    B --> [*]: yes
    B --> A: no

    A: "Activate RDS"?
    B: Owncloud OAuth redirect
  }

  state Zenodo {
    [*] --> M
    M --> N: Button pressed
    N --> [*]: yes
    N --> M: no

    M: "Activate Zenodo?"
    N: Zenodo OAuth redirect
  }
```

### Reference to Token Service on level 2

The background flow of the input masks is strongly influenced by the corresponding use case service. Therefore you have to look at the [Token Services]/doc/impl/use-cases/port-service/#communication-with-the-plugins) page.

Note: This reference will disappear in the future, as the Token Service will be removed and the task will be taken over by the Token Storage on level 3 to define clearer tasks.

## Projects

In order to be able to use the tokens in the previous section in a meaningful way and thus implement workflows between the services, projects are created which represent these connections. For this purpose, the user is presented with an input mask. The following status diagram shows the queries.

### Overview page

The user has an overview page at the beginning, which is empty. He has the possibility to create a new project, with which he is forwarded to the input mask, which follows the following state diagram.

### Input mask for project creation

At any time the user can leave his current status and return to the overview. His previous information is not deleted, but the status is maintained until he completes or deletes the project.

``mermaid
stateDiagram

Service: "Connect services".
Metadata: "Select / enter metadata
Files: "Synchronize files".

[*] --> Service: Create project
Service --> Metadata: Saving Services
Metadata --> files: Saving Metadata
Files --> [*]: Complete / publish project

Metadata --> Service: Revise services
Files --> Metadata: Revise Metadata
Files --> Service: Revise services

```

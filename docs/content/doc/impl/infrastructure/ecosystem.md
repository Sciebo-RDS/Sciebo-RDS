---
title: Service ecosystem
subtitle: 

menu:
  doc:
    parent: infrastructure
weight: 501
mermaid: true
---

## Diagram

The following diagram shows the data flow within the RDS ecosystem. Each service is linked, so from here you can quickly look up the corresponding documentation by clicking on the respective node.

Incoming connections are established by the plugins (currently Owncloud). Further integrations are possible. (Information about this will be added later).

```mermaid
graph TD;
  %% define nodes

  subgraph Plugins
      OP[Owncloud App]
  end


  subgraph RDS
    Ingress

    subgraph Adapters & Ports
      %% SPAEx[SPA Exporter]
      %% SPATS[SPA Token Storage]

      PInvenio[Port Invenio]
      POwncloud[Port Owncloud]

      subgraph Use Cases
        UCExporter[Exporter Service]
        UCPort[Port Service]
        UCMetadata[Metadata Service]
        %% UCProject[Project Service]

        subgraph Central Services
          CSToken[Token Storage]
          CSProject[Research Manager]
        end
      end
    end
  end

  WWWI[incoming connections]
  WWWO[outgoing connections]

  click PInvenio "/doc/impl/ports/port-invenio"
  click POwncloud "/doc/impl/ports/port-storage"

  click UCPort "/doc/impl/use-cases/port-service"
  click UCExporter "/doc/impl/use-cases/exporter"
  click UCMetadata "/doc/impl/use-cases/metadata"

  click CSProject "/doc/impl/central/research-manager"
  click CSToken ""/doc/impl/central/token-storage""

  %% define connections
  WWWI --> OP
  OP --> Ingress

  %% Ingress --> SPAEx --> UCExporter
  %% Ingress --> SPATS --> CSToken
  %% Ingress -->|Nur für die Registration von neuen Tokens| ARegister
  Ingress --> CSProject & UCExporter & UCMetadata & UCPort

  %% UCExporter --> UCProject
  %% UCProject --> CSProject
  UCPort --> CSToken

  CSToken --- PInvenio & POwncloud
  UCExporter & UCMetadata --> PInvenio & POwncloud & CSProject

  %% PInvenio --> POwncloud

  PInvenio --> WWWO
  POwncloud --> WWWO
```

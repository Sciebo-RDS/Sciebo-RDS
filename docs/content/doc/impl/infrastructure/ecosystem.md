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
      OP[Frontend App]
  end

  subgraph RDS
    Ingress[Backend Edge Server]

    subgraph Adapters & Ports
      %% SPAEx[SPA Exporter]
      %% SPATS[SPA Token Storage]

      PInvenio[Port Zenodo]
      POwncloud[Port Owncloud]
      POSF[Port OSF]
      PReva[Port Reva]
      PDatasafe[Port Datasafe]

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

  click OP "/doc/impl/plugins/owncloud/"

  click PInvenio "/doc/impl/ports/port-invenio"
  click POwncloud "/doc/impl/ports/port-storage"
  click PReva "https://github.com/Sciebo-RDS/port-reva"
  click POSF "/doc/impl/ports/port-osf"
  click PDatasafe "https://github.com/Sciebo-RDS/port_datasafe"

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

  CSToken --- PInvenio & POwncloud & PReva & POSF & PDatasafe
  UCExporter & UCMetadata & UCPort --> PInvenio & POwncloud & PReva & POSF & PDatasafe & CSProject & CSToken

  PInvenio & PDatasafe & POwncloud & PReva & POSF --> WWWO
```

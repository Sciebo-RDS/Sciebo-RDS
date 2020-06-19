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

``mermaid
graph TD;
  %% define nodes

  WWWI [incoming connections]

  subgraph RDS
    Ingress

    subgraph Adapters & Ports
      %% SPAEx [SPA Exporter]
      %% SPATS [SPA Token Storage]

      PInvenio [Port Invenio]
      POwncloud [Port Owncloud]

      subgraph Use Cases
        UCExporter [Exporter Service]
        UCPort [Port Service]
        UCMetadata [Metadata Service]
        %% UCProject [Project Service]

        subgraph Central Services
          CSToken [Token Storage]
          CSProject [Research Manager]
        end
      end
    end
  end

  WWWO [outgoing connections]

  click PInvenio "/en/doc/impl/ports/port-invenio
  click POwncloud "/en/doc/impl/ports/port-storage

  click UCPort "/en/doc/impl/use-cases/port-service
  click UCExporter "/en/doc/impl/use-cases/exporter
  click UCMetadata "/en/doc/impl/use-cases/metadata

  click CSProject "/en/doc/impl/central/research-manager"
  click CSToken ""/en/doc/impl/central/token-storage""

  %% define connections
  WWWI --> Ingress

  %% Ingress --> SPAEx --> UCExporter
  %% Ingress --> SPATS --> CSToken
  %% Ingress -->|Only for the registration of new tokens| ARegister
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

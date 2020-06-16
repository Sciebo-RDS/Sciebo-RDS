---
title: Service Ökosystem
subtitle: Wo befindet sich was

menu:
  doc:
    parent: arch
weight: 205
mermaid: true
---

## Diagramm

Das folgende Diagramm zeigt den Datenfluss innerhalb des Service Ökosystems. Jeder Service ist verlinkt, sodass man von hier aus sehr schnell in die entsprechende Dokumentation schauen kann, indem man auf den jeweiligen Knoten drückt.

```mermaid
graph TD;
  %% define nodes

  WWWI[hereinkommende Verbindungen]

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
          CSProject[Project Manager]
        end
      end
    end
  end

  WWWO[ausgehende Verbindungen]

  click SPAEx "/de/doc/impl/adapters/spa-exporter/"
  click SPATS "/de/doc/impl/adapters/spa-token-storage"
  click UCExporter "/de/doc/impl/use-cases/exporter"
  click UCPort "/de/doc/impl/use-cases/port-service"
  click CSProject "/de/doc/impl/central/research-manager"
  click PInvenio "/de/doc/impl/ports/port-invenio"
  click POwncloud "/de/doc/impl/ports/port-storage"

  %% define connections
  WWWI --> Ingress

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

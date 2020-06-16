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

Das folgende Diagramm zeigt den Datenfluss innerhalb des RDS Ökosystems. Jeder Service ist verlinkt, sodass man von hier aus sehr schnell in die entsprechende Dokumentation schauen kann, indem man auf den jeweiligen Knoten drückt.

Hereinkommende Verbindungen werden u.a. von den Plugins aufgebaut (aktuell Owncloud). Weitere Integrationen sind möglich. (Informationen hierzu werden noch nachgetragen.)

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

  click PInvenio "/de/doc/impl/ports/port-invenio"
  click POwncloud "/de/doc/impl/ports/port-storage"

  click UCPort "/de/doc/impl/use-cases/port-service"
  click UCExporter "/de/doc/impl/use-cases/exporter"
  click UCMetadata "/de/doc/impl/use-cases/metadata"

  click CSProject "/de/doc/impl/central/research-manager"
  click CSToken ""/de/doc/impl/central/token-storage""

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

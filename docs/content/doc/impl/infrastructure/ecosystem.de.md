---
title: Service Ökosystem
subtitle: Wo befindet sich was

menu:
  doc:
    parent: infrastructure
weight: 501
mermaid: true
---

## Diagramm

Das folgende Diagramm zeigt den Datenfluss innerhalb des RDS Ökosystems. Jeder Service ist verlinkt, sodass man von hier aus sehr schnell in die entsprechende Dokumentation schauen kann, indem man auf den jeweiligen Knoten drückt.

Hereinkommende Verbindungen werden u.a. von den Plugins aufgebaut (aktuell Owncloud). Weitere Integrationen sind möglich. (Informationen hierzu werden noch nachgetragen.)

```mermaid
graph TD;
  %% define nodes
  
  subgraph Plugins
      OP[Owncloud App]
  end

  subgraph "RDS (Layer0)"
    Ingress[Ingress]
    Describo[Describo Online]
    Web[RDS Web]
    Helper[RDS Token Updater]
    DescriboDB[PostgreSQL Datenbank]
    RedisH[Redis Master Helper]

    subgraph "Adapters & Ports (Layer1)"
      PInvenio[Port Zenodo]
      POwncloud[Port Owncloud]
      POSF[Port OSF]
      PReva[Port Reva]
      PDatasafe[Port Datasafe]

      subgraph "Use Cases (Layer2)"
        UCExporter[Exporter Service]
        UCPort[Port Service]
        UCMetadata[Metadata Service]
        %% UCProject[Project Service]

        subgraph "Central Services (Layer3)"
          Redis[Redis Cluster]
          CSToken[Token Storage]
          CSProject[Research Manager]
        end

        Centralservices(" ")
        Ports(" ")
      end
    end
  end

  WWWI[hereinkommende Verbindungen]
  WWWO[ausgehende Verbindungen]

  click OP "/de/doc/impl/plugins/owncloud/"
  click Describo "https://github.com/Arkisto-Platform/describo-online"
  click Helper "https://github.com/Sciebo-RDS/RDS-Web/tree/rework/helper"
  click Web "https://github.com/Sciebo-RDS/RDS-Web"

  click PInvenio "/de/doc/impl/ports/port-invenio"
  click POwncloud "/de/doc/impl/ports/port-storage"
  click PReva "https://github.com/Sciebo-RDS/port-reva"
  click POSF "/de/doc/impl/ports/port-osf"
  click PDatasafe "https://github.com/Sciebo-RDS/port_datasafe"

  click UCPort "/de/doc/impl/use-cases/port-service"
  click UCExporter "/de/doc/impl/use-cases/exporter"
  click UCMetadata "/de/doc/impl/use-cases/metadata"

  click CSProject "/de/doc/impl/central/research-manager"
  click CSToken "/de/doc/impl/central/token-storage"

  %% define connections
  WWWI --> OP
  OP --> Ingress --> Describo & Web

  Web --> CSProject & UCExporter & UCMetadata & UCPort & Describo
  CSToken & UCExporter & UCMetadata & UCPort --- Ports
  UCExporter & UCMetadata & UCPort --- Centralservices
  Ports --> PInvenio & POwncloud & PReva & POSF & PDatasafe
  Centralservices --> CSProject & CSToken

  CSProject --> Redis

  Helper --> Describo & RedisH
  CSToken --> RedisH & Redis
  Describo --> DescriboDB

  PInvenio & PDatasafe & POwncloud & PReva & POSF --> WWWO

classDef SkipLevel width:0px;
class Ports,Centralservices SkipLevel
```

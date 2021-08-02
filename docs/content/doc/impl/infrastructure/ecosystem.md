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

  WWWI[incoming connections]
  WWWO[outgoing connections]

  click OP "/doc/impl/plugins/owncloud/"
  click Describo "https://github.com/Arkisto-Platform/describo-online"
  click Helper "https://github.com/Sciebo-RDS/RDS-Web/tree/rework/helper"
  click Web "https://github.com/Sciebo-RDS/RDS-Web"

  click PInvenio "/doc/impl/ports/port-invenio"
  click POwncloud "/doc/impl/ports/port-storage"
  click PReva "https://github.com/Sciebo-RDS/port-reva"
  click POSF "/doc/impl/ports/port-osf"
  click PDatasafe "https://github.com/Sciebo-RDS/port_datasafe"

  click UCPort "/doc/impl/use-cases/port-service"
  click UCExporter "/doc/impl/use-cases/exporter"
  click UCMetadata "/doc/impl/use-cases/metadata"

  click CSProject "/doc/impl/central/research-manager"
  click CSToken "/doc/impl/central/token-storage"

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

# Internal Microservices

The following diagram shows the data flow within the RDS ecosystem. Each service is linked, you can quickly look up the corresponding documentation by clicking on the respective node.
Incoming connections are established by the EFSS plugin (e.g. Owncloud).

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

  click OP "/impl/plugins/owncloud/"
  click Describo "https://github.com/Arkisto-Platform/describo-online"
  click Helper "https://github.com/Sciebo-RDS/RDS-Web/tree/rework/helper"
  click Web "https://github.com/Sciebo-RDS/RDS-Web"

  click PInvenio "/impl/layer1-port-invenio-docstring"
  click POwncloud "/impl/layer1-port-storage-docstring"
  click PReva "https://github.com/Sciebo-RDS/port-reva"
  click POSF "/impl/layer1-port-osf-docstring"
  click PDatasafe "https://github.com/Sciebo-RDS/port_datasafe"

  click UCPort "/impl/layer2-port-service-docstring"
  click UCExporter "/impl/layer2-exporter-service-docstring"
  click UCMetadata "/impl/layer2-metadata-service-docstring"

  click CSProject "/impl/layer3-research-manager-docstring"
  click CSToken "/impl/layer3-token-storage-docstring"

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
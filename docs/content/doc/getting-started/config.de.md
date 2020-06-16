---
title: Konfiguration
subtitle: Wie konfiguriert man RDS

menu:
  doc:
    parent: installation
weight: 100
---

Man benötigt den Ordner "deploy" aus dem Github Repositorium.

```bash
git clone https://github.com/Sciebo-RDS/Sciebo-RDS.git
cd ScieboRDS/deploy
```

Darin sind sämtliche Dateien enthalten, welche zur Konfiguration und Installation benötigt werden.

Um die Installation anzupassen, sind mehrere Dateien anzupassen. Dafür liegen im deploy- und in den jeweiligen Microservice-Ordnern ".example"-Dateien, welche kopiert und umbenannt werden sollen und anschließend angepasst werden müssen.

```bash
cp kustomization.yaml.example kustomization.yaml
nano kustomization.yaml
```

In der kustomization.yaml werden die Proxies definiert, welche möglicherweise in der Umgebung notwendig sind. Dadurch können die Microservices auch außerhalb des Clusters verfügbare Services erreichen, falls der Cluster keine eigene weltweite IP besitzt.

Die folgenden Services benötigen ebenfalls Anpassungen, wenn sie eingesetzt werden sollen:
- Owncloud (circle1_port_owncloud)  
- Zenodo (circle1_port_zenodo)

In den Ordner sind wieder "example"-Dateien enthalten, genauer "values.yaml.example", welche wie oben umbenannt werden müssen. Darin müssen nun die entsprechenden Daten für die Services eingegeben werden.

```bash
cp values.yaml.example values.yaml
nano values.yaml
```

Sobald diese Anpassungen getätigt wurden, kann nun der Cluster installiert werden.

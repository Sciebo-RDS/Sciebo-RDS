---
title: Port OpenScienceFramework
subtitle: Exportiere deine Dateien zu einem OpenScienceFramework Repositorium.

menu:
  doc:
    parent: adapter-port
weight: 601
---

# Aufgabe

Dieser Service übernimmt sämtliche Kommunikation mit der konfigurierten OpenScienceFramework Instanz und stellt dessen Dateien dem RDS-System zur Verfügung.

Bei der Erstellung von Forschungsprojekten kann dieser Dienst kann als Quell- und Zieldienst konfiguriert werden.

## OpenAPI v3

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle2_use_cases/interface_port_metadata.yml"  >}}

## Implementierung

{{% code file="doc/impl/ports/port-osf-docstring.md" %}}

---
title: Port Zenodo
subtitle: Exportiere deine Dateien zu einem Zenodo Repositorium.

menu:
  doc:
    parent: adapter-port
weight: 601
---

# Aufgabe

Dieser Service übernimmt sämtliche Kommunikation mit der konfigurierten Owncloud-Instanz und stellt dessen Dateien dem RDS-System zur Verfügung.

Bei der Erstellung von Forschungsprojekten kann dieser Dienst kann als Quell- und Zieldienst konfiguriert werden.

## OpenAPI v3

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle2_use_cases/interface_port_metadata.yml"  >}}

## Implementierung

Die folgende Klasse implementiert eine Bibliothek, um die Invenio-Installation "Zenodo" verwenden zu können.

{{% code file="doc/impl/ports/port-invenio-docstring.md" %}}

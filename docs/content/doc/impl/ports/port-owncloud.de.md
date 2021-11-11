---
title: Port Owncloud
subtitle: Arbeite auf deinen Owncloud Dateien in RDS.

menu:
  doc:
    parent: adapter-port
weight: 600
---

# Aufgabe

Dieser Service übernimmt sämtliche Kommunikation mit der konfigurierten Owncloud-Instanz und stellt dessen Dateien dem RDS-System zur Verfügung.

Aktuell kann dieser Service bei der Konfiguration von Forschungsprojekten lediglich als Quelldienst verwendet werden, da aktuell nur der Download von Dateien implementiert ist.

## OpenAPI v3

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle2_use_cases/interface_port_file_storage.yml"  >}}

## Implementierung

Die folgende Klasse implementiert eine Bibliothek, um eine Owncloud-Installation verwenden zu können.

{{% code file="doc/impl/ports/port-owncloud-docstring.md" %}}
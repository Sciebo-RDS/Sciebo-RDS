---
title: Exporter Service
subtitle: Für das Exportieren und Importieren von Daten durch die Ports

menu:
  doc:
    parent: use-case
weight: 1000
mermaid: True
---

# Aufgabe

Der Exporter Service sorgt dafür, dass das Integrationsplugin nur wenige Endpunkte aufrufen muss und viele verschiedene Funktionalitäten nur dem RDS-System zur Verfügung stehen. Dadurch ist sichergestellt, dass keine Informationen nach Außen zur Verfügung stehen, solange die Authentifikation durch das Plugin sichergestellt ist.

Die Exportierung von Dateien wird auf Grundlage von vorher eingestellten Forschungsprojekten im Research Manager vollzogen.

Der Service kann auch als Importierer verwendet werden, indem die Exportierservices im entsprechenden Forschungsprojekt vertauscht werden (solange der Service dies unterstützt).

## OpenAPI

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle2_use_cases/exporter/use-case_exporter.yml"  >}}

{{% code file="doc/impl/use-cases/exporter-service-docstring.md" %}}

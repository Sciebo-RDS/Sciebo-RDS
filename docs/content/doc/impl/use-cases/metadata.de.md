---
title: Metadata Service
subtitle: Für die Verbindung und Erhalt der Metadaten aus den Ports.

menu:
  doc:
    parent: use-case
weight: 702
mermaid: True
---

# Aufgabe

Der Metadata Service sorgt dafür, dass das Integrationsplugin nur wenige Endpunkte aufrufen muss und viele verschiedene Funktionalitäten nur dem RDS-System zur Verfügung stehen. Dadurch ist sichergestellt, dass keine Informationen nach Außen zur Verfügung stehen, solange die Authentifikation durch das Plugin sichergestellt ist.

Dieser Dienst stellt Funktionen zur Anzeige und Bearbeitung von Metadaten für Dateien und Forschungsprojekten bereit. Dabei übernimmt er sämtliche Anfragen an die entsprechenden Ports, sodass das Plugins lediglich einen Endpunkt aufrufen muss und alle weiteren Aufrufe RDS-intern ausgelöst werden auf Grundlage des hinterlegten Forschungsprojekts.

## OpenAPI

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/informations-ep/RDS/circle2_use_cases/metadata/use-case_metadata.yml"  >}}

{{% code file="doc/impl/use-cases/metadata-service-docstring.md" %}}

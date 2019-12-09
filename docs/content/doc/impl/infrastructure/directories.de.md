---
title: Pfaddefinitionen
subtitle: Wo gibt es welchen Dienst zu finden

menu:
  doc:
    parent: infrastructure
mermaid: true
weight: 500
---

## Domain

Die Domain wird in der zentralen Konfigurationsdatei, [wie hier beschrieben](/de/doc/getting-started/config/), definiert. Die folgende Definitionen werden als Ordner unter dieser Domain angegeben. Falls Ihre Domain `example.com` lautet, dann ist ein beispielhafter Ordner `folder` wie folgt aufzufinden: `example.com/folder`.

## Pfaddefinierungen

Die folgenden Pfaddefinierungen werden von den jeweiligen Diensten ausdefiniert.

<center>

|     Dienst      |    Pfadangabe    |
|-----------------|------------------|
|  Token-Storage  |  /token-storage  |
|    Exporter     |    /exporter     |
|    Importer     |    /importer     |
|    Archiver     |    /archiver     |
| Project-Manager | /project-manager |

</center>

Die dienstspezifischen Unterordner und Endpunkte werden in den jeweiligen OpenAPI-Datei definiert und können in dieser Dokumenation eingesehen werden. Zu beachten gilt die folgende Einschränkung.

### Single-Page Application

Die SPA (Single-Page Application), welche durch die Dienste mitgebracht werden, werden auch unter den genannten Pfadangaben abgerufen. Dabei ist der Unterordner `web` unter der jeweiligen Pfadangabe für die SPA reserviert, worunter der SPA-Dienst Dateien wie `hypertext markup language` (html), `javascript` (js) und `cascading stylesheets` (css) ausgeliefert werden.

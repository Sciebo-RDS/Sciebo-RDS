---
title: Pfaddefinitionen
subtitle: Hier erfährst Du, welcher Microservice sich hinter den verschiedenen API-Endpunkten versteckt.

menu:
  doc:

    parent: infrastructure

mermaid: true
weight: 500
---

## Domain

Die Domain wird in der zentralen Konfigurationsdatei, [wie hier beschrieben](/de/doc/getting-started/config/), definiert. Die folgende Definitionen werden als Ordner unter dieser Domain angegeben. Falls Ihre Domain `example.com` lautet, dann ist ein beispielhafter Service `folder` wie folgt aufzufinden: `example.com/folder` .

## Pfaddefinierungen

Die folgenden Pfaddefinierungen werden von den jeweiligen Diensten ausdefiniert und sind somit von außen zu erreichen.

| Dienst          | Pfadangabe |
| --------------- | ---------- |
| RDS Web         | /          |
| Describo Online | /describo  |

Die dienstspezifischen Unterordner und Endpunkte werden in den jeweiligen OpenAPI-Datei definiert und können in dieser Dokumenation eingesehen werden.

In einer früheren Version gab es wesentlich mehr Dienste, welche nach außen verfügbar waren. Dies wurde aber geändert, um eine einfachere und sicherere Handhabung durch den RDS Web Dienst zu gewährleisten.

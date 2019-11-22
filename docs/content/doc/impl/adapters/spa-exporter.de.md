---
title: SPA Exporter
subtitle: Der ausliefernde Service.

menu:
  doc:
    parent: adapter-port
weight: 900
mermaid: true
---

## Minimaler Datensatz

Erstes Inkrement unterstützt nur minimaler Datensatz.
Der minimale Datensatz besteht aus den folgenden Informationen, welche der Entität [Deposit Metadata](https://developers.zenodo.org/#representation) entspricht:

|       Name       |    Typ     |                           Beschreibung                           |
|------------------|------------|------------------------------------------------------------------|
|      titel       |   String   |                     Der Titel der Deposition                     |
|   description    |   String   |                 Eine Beschreibung der Deposition                 |
| publication_date |    Date    | Ein Datumsobjekt, welches den Veröffentlichungszeitpunkt angibt. |
|   upload_type    | Enumerator |      Die Art der Deposition (Vortrag, Paper, Poster, etc.)       |

## DEA der Eingabemasken

Der Ablauf der Eingabemasken des Adapters für den Zenodo Services werden durch den folgenden DEA dargestellt.

```mermaid
stateDiagram
  [*] --> A
  A --> B: nicht valide
  B --> C: valide
  C --> D: bestätigen
  D --> E: Dateien ausgewählt
  E --> F: bei Erfolg
  E --> E: Warten
  F --> G: JA
  F --> H: NEIN
  G --> [*]
  H --> [*]
  B --> A: Zurücksetzen
  C --> A: Zurücksetzen
  D --> F: Keine Daten ausgewählt
  A --> C: valide

  A: Datensatz abfragen
  B: Fehlende Informationen einfordern
  C: eingegebene Daten anzeigen
  D: Datenauswahl anzeigen
  E: Uploadstatus rückmelden
  F: Soll die Deposition veröffentlich werden?
  G: Publiziert
  H: nicht publiziert
```

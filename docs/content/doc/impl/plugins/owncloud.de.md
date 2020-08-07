---
title: ownCloud
subtitle: RDS mittels ownCloud App integrieren und verwenden

menu:
  doc:
    parent: plugins
weight: 1200
mermaid: true
---

Dieser Plugin stellt die erste Integration von RDS in ein anderes Ökosystem dar. Um die Bedienbarkeit zu gewährleisten und möglichst niedrigschwellig zu gestalten, wird darauf geachtet, möglichst sämtliche Funktionsmöglichkeiten der Plattform zu verwenden und durch RDS zu erweitern.

# Installation

Das Plugin liegt im [Git-Repo im Ordner plugins](https://github.com/Sciebo-RDS/Sciebo-RDS/tree/master/plugins/ownCloud). Das Repositorium muss kopiert und anschließend der *rds*-Ordner in den *Apps*-Ordner der Owncloud-Instanz verschoben werden.

{{<callout "info">}}
Aktuell ist das RDS Plugin nicht im offiziellen Owncloud Marketplace für Apps verfügbar. Dies ist aktuell in Vorbereitung. Daher sind die manuellen Schritte notwendig.
{{</callout>}}

Die folgenden Befehle kopieren das Git-Repo in den aktuellen Ordner und kopieren die notwendigen Dateien. Angenommen wird, dass die Owncloud-Instanz sich unter */var/www/html/owncloud* befindet. Dies kann in der ersten Zeile angepasst werden.

```bash
export OWNCLOUD_INSTALLATION=/var/www/html/owncloud
git clone https://github.com/Sciebo-RDS/Sciebo-RDS.git
cp -r Sciebo-RDS/plugins/ownCloud/rds $OWNCLOUD_INSTALLATION/apps/
```

Nun kann die *RDS*-App in den Einstellungen aktiviert (https://localhost/owncloud/index.php/settings/admin?sectionid=apps&category=disabled) werden. Anschließend muss der Administrator in den Administratoreneinstellungen die RDS App konfigurieren, wie im folgenden beschrieben.

### Einstellungen Administratorensicht

Sobald das Plugin in Owncloud aus dem Apps Market installiert und aktiviert wurde (siehe [hier wie](https://doc.owncloud.com/server/admin_manual/installation/apps_management_installation.html)), muss das RDS System in den Einstellungen konfiguriert werden.

![Administratorensicht](/images/oc-plugin-view-admin.png)

### Einstellungen Nutzersicht

In den Einstellungen hat der Nutzer die Möglichkeit, OAuth Tokens und Passwörter (welche ebenfalls als Tokens bezeichnet werden im Folgenden) im System zu hinterlegen, womit sich das System im Namen des Nutzers bei verschiedenen Diensten anmelden kann. Das folgende Zustandsdiagramm stellt den Ablauf dar.

### Eingabemasken der Einstellungen

```mermaid
stateDiagram
  [*] --> Start
  Start --> RDS: nein
  Start --> Z: ja
  Z --> Zenodo: nein
  Z --> [*]: ja

  RDS --> Start
  Zenodo --> Start

  Start: RDS aktiviert?
  Z: Zenodo aktiviert?

  state RDS {
    [*] --> A
    A --> B: Knopf gedrückt
    B --> [*]: ja
    B --> A: nein

    A: "RDS aktivieren?"
    B: Owncloud OAuth redirect
  }

  state Zenodo {
    [*] --> M
    M --> N: Knopf gedrückt
    N --> [*]: ja
    N --> M: nein

    M: "Zenodo aktivieren?"
    N: Zenodo OAuth redirect
  }
```

### Verweis auf Token Service auf Ebene 2

Der hintergründige Ablauf der Eingabemasken wird stark durch den entsprechenden Use-Case Dienst beeinflusst. Dafür muss man auf jedenfall die Seite des [Token Services](/de/doc/impl/use-cases/port-service/#kommunikation-mit-den-plugins) betrachten.

Notiz: Dieser Verweis wird in Zukunft verschwinden, da der Token Service entfernt wird und die Aufgabe vom Token Storage auf Ebene 3 übernommen wird, um klarere Aufgabenbereiche abzustecken.

## Projekte

Um die Tokens im vorherigen Abschnitt auch sinnvoll verwenden zu können und somit Workflows zwischen den Diensten implementieren zu können, werden Projekte angelegt, welche diese Zusammenhänge darstellen. Dafür bekommt der Nutzer wiederum eine Eingabemaske angezeigt. Das folgeden Zustandsdiagramm stellt die Abfragen dar.

### Übersichtsseite

Der Nutzer hat zu Beginn eine Übersichtsseite, welche leer ist. Er hat die Möglichkeit ein neues Projekt zu erstellen, womit er zur Eingabemaske weitergeleitet werden, welche folgendes Zustandsdiagramm verfolgt.

### Eingabemaske zur Projekterstellung

Jederzeit kann der Nutzer seinen aktuellen Stand verlassen und zur Übersicht zurückkehren. Seine bisherigen Angaben werden dabei nicht gelöscht, sondern der Zustand wird beibehalten bis er das Projekt abschließt oder löscht.

```mermaid
stateDiagram

Dienst: "Dienste verbinden"
Metadaten: "Metadaten auswählen / eingeben"
Dateien: "Dateien abgleichen"

[*] --> Dienst: Projekt erstellen
Dienst --> Metadaten: Dienste abspeichern
Metadaten --> Dateien: Metadaten abspeichern
Dateien --> [*]: Projekt abschließen / veröffentlichen

Metadaten --> Dienst: Dienste überarbeiten
Dateien --> Metadaten: Metadaten überarbeiten
Dateien --> Dienst: Dienste überarbeiten

```

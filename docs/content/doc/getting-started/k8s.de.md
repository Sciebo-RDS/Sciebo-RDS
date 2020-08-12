---
title: Kubernetes
subtitle: Helm Chart und Installationsanleitung

menu:
  doc:

    parent: installation

weight: 302
---

{{<callout "warning">}}
In diesem Kapitel werden einige Konfigurationen benötigt, welche durch das vorherige Kapitel vollzogen wurden. Falls die erforderlichen Dateien und Informationen nicht vorhanden sind, wird es zu Fehlermeldungen kommen. Es bereits die [Konfigurationsanleitung](/de/doc/getting-started/config/) ausgeführt worden sein.
{{</callout>}}

Nun kann mit folgendem Befehl das RDS-Ökosystem auf den Cluster geladen werden:

``` bash
make install
```

Da nun die Installation der RDS-Instanz abgeschlossen ist, wird nun eine Clientsoftware benötigt. Aktuell werden folgende Plugins angeboten:

- [ownCloud Plugin](/de/doc/impl/plugins/owncloud/)

### Überwachung

Das System installiert automatisch eine Jaeger-Instanz für das Verfolgen von Log-Nachrichten. Darauf kann man mit folgendem Befehl zugreifen und anschließend im Browser die angezeigte IP-Adresse aufrufen:

``` bash
make jaeger
```

Jaeger eignet sich besonders gut für die Identifizierung von Fehlern oder Problemen innerhalb des Ökosystems.

Wird ein Prometheus-System verwendet, so werden automatisch sämtliche Metriken abgegriffen und im jeweiligen System angeboten. Eine standardisierte Sicht wird in Zukunft angeboten (siehe [Issue 39](https://github.com/Sciebo-RDS/Sciebo-RDS/issues/39)).

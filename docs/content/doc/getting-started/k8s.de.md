---
title: Kubernetes
subtitle: Helm Chart und Installationsanleitung

menu:
  doc:

    parent: installation

weight: 302
---

Voraussetzung: [Konfiguration getätigt](/de/doc/getting-started/config/)

Im "deploy"-Ordner ist eine Makefile, welche mit dem Programm *make* benutzt wird.

``` bash
sudo apt install make
```

Falls helm oder kubectl noch nicht installiert wurden, können diese bequem installiert werden.

{{<tabs>}}
{{<tab "bash" "Ubuntu/Debian">}}make dependencies_ubuntu
{{</tab>}}

{{<tab "bash" "Fedora/CentOS">}}make dependencies_fedora
{{</tab>}}
{{</tabs>}}

{{<callout "tip">}}
Hinweis: Seit Helm v3 wird kein Tillerserver mehr auf Seiten des Kubernetes [benötigt](https://helm.sh/blog/helm-3-released/).
{{</callout>}}

Nun muss Kubectl konfiguriert werden, sodass auf ein Kubernetes-Cluster zugegriffen werden kann. (Für Testzwecke minikube nutzen, andernfalls den Clusteradministrator nachfragen.)

Anschließend kann mit folgendem Befehl das RDS Ökosystem auf den Cluster geladen werden:

``` bash
make install
```

Durch den oberen Befehl werden sämtliche zur Verfügung stehende Services installiert. Aktuell wird noch nicht überprüft, welche Services konfiguriert wurden, damit nur diese auch aufgesetzt werden. Das bedeutet aktuell, dass nicht konfigurierte Dienste nicht funktionieren, aber aufgesetzt werden.

{{<callout "warning">}}
Sollte die Fehlermeldung *Error: template: circle2-port-service/templates/tests/test-connection.yaml:14:73: executing "circle2-port-service/templates/tests/test-connection.yaml" at <.Values.service.port>: nil pointer evaluating interface {}.port* in einer Abwandlung auftreten, so ist keine values.yaml Datei vorhanden für den genannten Service. Schaue dafür nochmal in der [Konfiguration](/de/doc/getting-started/config/) nach.
{{</callout>}}

Das System installiert automatisch eine Jaeger-Instanz für das Verfolgen von Log-Nachrichten. Darauf kann man mit folgendem Befehl zugreifen und anschließend im Browser die angezeigte IP-Adresse aufrufen:

``` bash
make jaeger
```

Jaeger eignet sich besonders gut für die Identifizierung von Fehlern oder Problemen innerhalb des Ökosystems.

Wird ein Prometheus-System verwendet, so werden automatisch sämtliche Metriken abgegriffen und im jeweiligen System angeboten. Eine standardisierte Sicht wird in Zukunft angeboten (siehe [Issue 39](https://github.com/Sciebo-RDS/Sciebo-RDS/issues/39)).

Da nun die Installation der RDS-Instanz abgeschlossen ist, wird nun eine Clientsoftware benötigt. Aktuell werden folgende Plugins angeboten:

- [ownCloud Plugin](/de/doc/impl/plugins/owncloud/)

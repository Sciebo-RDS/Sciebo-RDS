---
title: Kubernetes
subtitle: Helm Chart und Installationsanleitung

menu:
  doc:
    parent: installation

weight: 300
---

Nachfolgend wird gezeigt, wie das RDS System in einem Kubernetes Cluster installiert werden kann.

{{<callout "info">}}
Für einen Überblick über das RDS System und dessen Funktionsweise, sei auf diesen [Artikel](/de/page/about/) verwiesen.
{{</callout>}}

Zu Beginn dieser Anleitung werden die Voraussetzung an den Cluster und andere Software genannt, welche zuerst erfüllt sein müssen. Anschließend wird das RDS System konfiguriert, sodass es danach auf dem Kubernetes Cluster installiert werden kann.

## Voraussetzungen

Als Versionskontrollprogramm wird [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) verwendet.

Weiterhin wird ein [Kubernetes](https://kubernetes.io/docs/home/) ([lokale Installation via Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/), Windows WSL2 Integration[[1]](https://kubernetes.io/blog/2020/05/21/wsl-docker-kubernetes-on-the-windows-desktop/)[[2]](https://kubernetes.io/blog/2020/05/21/wsl-docker-kubernetes-on-the-windows-desktop/#minikube-kubernetes-from-everywhere)) Cluster benötigt, welches eine [Docker-kompatible Runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes/) anbietet.

Folgende Rechte muss der [Nutzeraccount](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) besitzen:
- Erzeugung von eigenen Deployments
- Erzeugung von eigenen Secrets
- Erzeugung von eigenen ConfigMaps
- Erzeugung von eigenen DaemonSets
- Erzeugung von eigenen Services

Diese Rechte sind vergleichsweise fundamental für die Arbeit mit Kubernetes und sollten für jedes Nutzerkonto verfügbar sein. Es kann dennoch in einigen Umgebungen nötig sein, den Clusteradministrator bezüglich der Vergabe dieser Rechte anzusprechen.

Die folgenden Rechte sind optional, aber sehr empfohlen:
- Erstellung von Namespaces

{{<callout "info">}}
Use minikube for test purposes, otherwise ask the cluster administrator for access informations.
Für Testzwecke wird `minikube` empfohlen. Ansonsten muss ein Cluster Administrator für Zugangsdaten kontaktiert werden.
{{</callout>}}

### Ingress

Das System benötigt einen Ingress Server. Sollte Minikube zum Einsatz kommen, lässt sich dies mit folgendem Befehl nachrüsten. Andernfalls bitte bei einem Administrator nachfragen.

```bash
minikube addons enable ingress
```

### Erforderliche Programme

Es wird das Programm `make` für die Konfiguration und Installation der Software verwendet. Die benötigte `Makefile` ist im `deploy` Ordner zu finden. Falls `helm` oder `kubectl` noch nicht installiert wurden, kann dies mit den folgenden Befehlen erledigt werden.

{{<tabs>}}
{{<tab "bash" "Ubuntu/Debian">}}sudo apt install make -y
make dependencies_ubuntu
{{</tab>}}

{{<tab "bash" "Fedora/CentOS">}}sudo dnf install make -y
make dependencies_fedora
{{</tab>}}

{{<tab "bash" "Windows 10 Powershell">}}Set-ExecutionPolicy AllSigned
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco install -y make
make dependencies_windows
{{</tab>}}
{{</tabs>}}

{{<callout "tip">}}
Hinweis: Seit Helm v3 wird kein Tillerserver mehr auf Seiten des Kubernetes [benötigt](https://helm.sh/blog/helm-3-released/).
{{</callout>}}

## Konfiguration


Man benötigt den Ordner "deploy" aus dem Github Repositorium.

```bash
git clone https://github.com/Sciebo-RDS/Sciebo-RDS.git
cd ScieboRDS/deploy
```

Darin sind sämtliche Dateien enthalten, welche zur Konfiguration und Installation benötigt werden.

{{<callout info>}}
Die Helm Charts können im [Repositorium](https://github.com/Sciebo-RDS/charts) eingesehen werden.
{{</callout>}}

Um die Installation anzupassen, sind mehrere Dateien anzupassen. Dafür liegen im `deploy` Ordner mehrere `.example` Dateien, welche kopiert und umbenannt werden sollen und anschließend ggfs. inhaltlich anzupassen sind.

```bash
cp configuration.yaml.example configuration.yaml
nano configuration.yaml
```

In der `configuration.yaml` werden u.a. die Proxies definiert, welche möglicherweise in der Umgebung notwendig sind. Dadurch können die Microservices auch außerhalb des Clusters verfügbare Services erreichen, falls der Cluster keine eigene weltweite IP besitzen sollte. Falls unbekannt, sollten Details zur Proxykonfiguration beim lokalen Netzwerkadministrator in Erfahrung gebracht werden können. 

Für alle Microservices, die eingesetzt werden sollen, gilt, dass potentiell weitere Anpassungen vorgenommen werden können und müssen. Falls die Standardwerte für den Einsatz ausreichen, so sind keine Änderungen notwendig, außer in den Konnektorendiensten. Um Werte abzuändern, ist eine `values.yaml` Datei notwendig. Um alle verfügbaren Parameter einzusehen, ist ein Blick in das [Helm Chart Repo](https://github.com/Sciebo-RDS/charts/tree/master/charts) empfohlen.

Da die Konnektorendienste zusätzliche Informationen zur OAuth-Authentifizierung benötigt wie die ID und das Secret, benötigen diese eine values.yaml Datei. 
Im `deploy` Ordner ist wieder eine `example`-Datei vorhanden, genauer `values.yaml.example`, welche wie oben beschrieben umbenannt werden müssen. Innerhalb der Datei können nun die entsprechenden Daten für die Services lokal angepasst werden, falls das nötig ist. 

```bash
cp values.yaml.example values.yaml
nano values.yaml
```

Sobald die Anpassungen getätigt wurden, kann das System installiert werden.


### Namespace

Es wird empfohlen einen eigenen [Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) für RDS im Kubernetes-Cluster zu erzeugen (z.B. *research-data-services*).

{{<callout warning>}}
Falls die folgenden Anweisungen nicht ausgeführt werden, müssen sämtliche Befehle entsprechend ergänzt werden und die im Folgenden zur Verfügung gestellten Hilfsmittel können nicht ohne Weiteres verwendet werden. Somit müssen sämtliche Befehle in der Datei `Makefile` angepasst oder manuell ausgeführt werden.
{{</callout>}}

Um einen Namespace zu erstellen, sollte die Datei `namespace.yaml.example` in `namespace.yaml` umbenannt werden. Die darin enthaltenen Informationen können mit dem folgenden Befehlen angewendet werden.

{{<tabs>}}
{{<tab "bash" "Apply namespace">}}cp namespace.yaml.example namespace.yaml
nano namespace.yaml
make install_namespace
kubectl config set-context --current --namespace=$(grep 'name:' namespace.yaml | tail -n1 | awk '{ print $2}')
{{</tab>}}

{{<tab "bash" "Remove namespace">}}kubectl config set-context --current --namespace=default
make uninstall_namespace
{{</tab>}}
{{</tabs>}}

Anschließend wird das Angeben eines Kontexts für jeden Aufruf des Kubectl-Befehls (auch: Helm) obsolet, da der angegebene Namespace als Default verwendet wird.

### Verschlüsselung

Falls die Kommunikation zwischen Plugins und Cluster durch eine HTTPS-Verbindung abgesichert werden soll, was dringend empfohlen wird, so kann mittels des Shellskriptes [create_certs.sh](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/master/deploy/create_certs.sh) ein entsprechendes Zertifikat erstellt und als Secret hinterlegt werden. Das Skript muss dahingehend angepasst werden, für welche Domain das Zertifikat ausgestellt werden soll.

Mit dem folgenden Befehlen können die benötigten Zertifikate erstellt und verwendet weden.

{{<tabs>}}
{{<tab "bash" "Create and apply ssl cert">}}cp create_certs.sh.example create_certs.sh
nano create_certs.sh
make install_tls
{{</tab>}}

{{<tab "bash" "Delete ssl cert">}}make uninstall_tls
{{</tab>}}
{{</tabs>}}

{{<callout info>}}
Ein bereits existierende Zertifikat sollte als `Secret` unter dem Namen `sciebords-tls-public` gespeichert werden. Das Skript `create_certs.sh` bietet hier ein Beispiel.
Falls ein anderer Name verwendet werden soll, kann der Name in der Datei `values.yaml` unter `global.ingress.tls.secretName` angegeben werden, sodass RDS dieses `Secret` nach einem Neustart verwendet.
{{</callout>}}

### Konfiguration anwenden

Sofern die vorherigen Schritte vollständig ausgeführt wurden, kann nun die Konfiguration auf den Cluster angewendet werden.

{{<tabs>}}
{{<tab "bash" "Apply configuration">}}make install_configuration
{{</tab>}}

{{<tab "bash" "Undoing configuration">}}make uninstall_configuration
{{</tab>}}
{{</tabs>}}


## Installation

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

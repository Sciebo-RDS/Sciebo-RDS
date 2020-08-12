---
title: Voraussetzungen
subtitle: Was wird benötigt, um RDS zu installieren.

menu:
  doc:
    parent: installation
weight: 300
---

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

---
title: Kubernetes
subtitle: Helm Chart und Installationsanleitung

menu:
  doc:
    parent: installation
weight: 102
---

Voraussetzung: Konfiguration getätigt

Im "deploy"-Ordner ist eine Makefile, welche mit dem Programm *make* benutzt wird.

```bash
sudo apt install make
```

Falls helm oder kubectl noch nicht installiert wurden, können diese bequem installiert werden.

Für Fedora/CentOS:

```bash
make dependencies_fedora
```

Für Ubuntu/Debian:

```bash
make dependencies_ubuntu
```

Nun muss Kubectl konfiguriert werden, sodass auf ein Kubernetes-Cluster zugegriffen werden kann. (Für Testzwecke minikube nutzen, andernfalls den Clusteradministrator nachfragen.)

Anschließend kann mit folgendem Befehl das RDS Ökosystem auf den Cluster geladen werden:

```bash
make install
```

Durch den oberen Befehl werden sämtliche zur Verfügung stehende Services installiert. Aktuell wird noch nicht überprüft, welche Services konfiguriert wurden, damit nur diese auch aufgesetzt werden. Das bedeutet aktuell, dass nicht konfigurierte Dienste nicht funktionieren, aber aufgesetzt werden.

Das System installiert automatisch eine Jaeger-Instanz für das Verfolgen von Log-Nachrichten. Darauf kann man mit folgendem Befehl zugreifen und anschließend im Browser die angezeigte IP-Adresse aufrufen:

```bash
make jaeger
```

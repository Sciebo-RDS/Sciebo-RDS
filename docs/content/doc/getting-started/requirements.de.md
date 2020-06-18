---
title: Voraussetzungen
subtitle: Was wird benötigt, um RDS zu installieren.

menu:
  doc:
    parent: installation
weight: 300
---

Als Versionskontrollprogramm wird [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) verwendet.

Weiterhin wird ein [Kubernetes](https://kubernetes.io/docs/home/) ([lokale Installation via Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/)) Cluster benötigt, welches eine [Docker-kompatible Runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes/) anbietet.

Folgende Rechte muss der [Nutzeraccount](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) besitzen:
- Erzeugung von eigenen Deployments
- Erzeugung von eigenen Secrets
- Erzeugung von eigenen ConfigMaps
- Erzeugung von eigenen DaemonSets
- Erzeugung von eigenen Services

Diese Rechte sind ziemlich fundamental für die Arbeit mit Kubernetes und sollten für jedes Nutzerkonto verfügbar sein. Es kann in einigen Umgebungen aber nötig sein, den Clusteradministrator auf diese Rechte anzusprechen und entsprechende Berechtigungen zu erhalten.

Es wird empfohlen einen eigenen [Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) für RDS im Kubernetes zu erzeugen (z.B. *research-data-services*).
Sobald Kubectl installiert ist ([siehe Kubernetes](/de/doc/getting-started/k8s/)) kann mittels folgendem Bashbefehl dieser Namespace Standard konfiguriert werden.

```bash
kubectl config set-context --current --namespace=research-data-services
```

Anschließend wird das Angeben eines Kontexts für jeden Kubectl Befehl (und Helm) obsolet, da der angegebene Namespace als Default verwendet wird. Ist dies nicht gewünscht, müssen sämtliche Befehle entsprechend ergänzt werden und die im Folgenden zur Verfügung gestellten Hilfsmittel können größtenteils nicht verwendet werden.

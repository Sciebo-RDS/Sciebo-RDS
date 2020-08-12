---
title: Requirements
subtitle: What do we need to install RDS

menu:
  doc:
    parent: installation
weight: 300
---

The version control program used is [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

Furthermore a [Kubernetes](https://kubernetes.io/docs/home/) ([local installation via Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/), Windows WSL2 Integration[[1]](https://kubernetes.io/blog/2020/05/21/wsl-docker-kubernetes-on-the-windows-desktop/)[[2]](https://kubernetes.io/blog/2020/05/21/wsl-docker-kubernetes-on-the-windows-desktop/#minikube-kubernetes-from-everywhere)) cluster is required, which offers a [Docker-compatible Runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)

The [user account](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) must have the following rights:
- Creation of own deployments
- Generation of own secrets
- Creation of own ConfigMaps
- Creation of own DaemonSets
- Generation of own services

These rights are rather fundamental for working with Kubernetes and should be available for every user account. However, in some environments, it may be necessary to contact the cluster administrator about these rights and obtain appropriate permissions.

The following rights are optional, but highly recommended:
- creation of Namespaces

{{<callout "info">}}
Use minikube for test purposes, otherwise ask the cluster administrator for access informations.
{{</callout>}}

The provided scripts uses *nano* to open files. Please be sure to installed it.

### Ingress

The system needs an ingress server. If you want to use minikube, you can add it with the following command. Otherwise, please ask your Kubernetes cluster administrator.

```bash
minikube addons enable ingress
```

---
title: Requirements
subtitle: What do we need to install RDS

menu:
  doc:
    parent: installation
weight: 300
---

The version control program used is [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

Furthermore a [Kubernetes](https://kubernetes.io/docs/home/) ([local installation via Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/), [Windows WSL2 Integration](https://kubernetes.io/blog/2020/05/21/wsl-docker-kubernetes-on-the-windows-desktop/)) cluster is required, which offers a [Docker-compatible Runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)

The [user account](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) must have the following rights:
- Creation of own deployments
- Generation of own secrets
- Creation of own ConfigMaps
- Creation of own DaemonSets
- Generation of own services

These rights are quite fundamental for working with Kubernetes and should be available for every user account. However, in some environments, it may be necessary to contact the cluster administrator about these rights and obtain appropriate permissions.

It is recommended to create a separate [namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) for RDS in Kubernetes (e.g. *research-data-services*).
As soon as Kubectl is installed ([see Kubernetes](/doc/getting-started/k8s/)), this namespace default can be configured with the following bash command

```bash
kubectl config set-context --current --namespace=research-data-services
```

After that, specifying a context for each Kubectl command (and helmet) becomes obsolete because the specified namespace is used as default. If this is not desired, all commands must be completed accordingly and the tools provided below cannot be used for the most part.

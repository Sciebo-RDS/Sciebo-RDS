---
title: Requirements
subtitle: What do we need to install RDS

menu:
  doc:
    parent: installation
weight: 300
---

The version control program used is [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

Furthermore a [Kubernetes](https://kubernetes.io/docs/home/) ([local installation via Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/), Windows WSL2 Integration[1](https://kubernetes.io/blog/2020/05/21/wsl-docker-kubernetes-on-the-windows-desktop/)[2](https://kubernetes.io/blog/2020/05/21/wsl-docker-kubernetes-on-the-windows-desktop/#minikube-kubernetes-from-everywhere)) cluster is required, which offers a [Docker-compatible Runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)

The [user account](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) must have the following rights:
- Creation of own deployments
- Generation of own secrets
- Creation of own ConfigMaps
- Creation of own DaemonSets
- Generation of own services

These rights are quite fundamental for working with Kubernetes and should be available for every user account. However, in some environments, it may be necessary to contact the cluster administrator about these rights and obtain appropriate permissions.

### Namespace

It is recommended to create a separate [namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) for RDS in Kubernetes (e.g. *research-data-services*).

Once Kubectl is installed ([see Kubernetes](/doc/getting-started/k8s/)) you can use the following bash commands to create a file named *namespace-rds.json*, create the namespace *research-data-services* in Kubernetes and configure it as the default in the current context

```bash
cat > namespace-rds.json << EOL
{
    "apiVersion": "v1",
    "kind": "Namespace",
    "metadata": {
        "name": "research-data-services",
        "labels": {
            "name": "research-data-services"
        }
    }
}
EOL
kubectl apply -f namespace-rds.json
kubectl config set-context --current --namespace=research-data-services
```

After that, specifying a context for each Kubectl command (and helmet) becomes obsolete because the specified namespace is used as default. If this is not desired, all commands must be completed accordingly and the tools provided below cannot be used for the most part.

### Ingress

The system needs an ingress server. If you want to use minikube, you can start such server with the following command. Otherwise please ask your kubernetes cluster.

```bash
minikube addons enable ingress
```

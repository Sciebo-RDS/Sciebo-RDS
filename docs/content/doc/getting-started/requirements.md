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

### Required programs

We use the program `make` to configure and deploy our software with a Makefile, which can be found in the `deploy` folder. If helm or kubectl have not yet been installed, you can easily install them with the following commands, too.

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
Note: Since Helm v3 no Tillerserver is [required](https://helm.sh/blog/helm-3-released/) on the Kubernetes side.
{{</callout>}}

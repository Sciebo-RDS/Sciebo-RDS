---
title: Kubernetes
subtitle: Helm Chart und Installationsanleitung

menu:
  doc:
    parent: installation
weight: 302
---


Condition: [Configuration made]/doc/getting-started/config/)

In the "deploy" folder is a Makefile, which is used with the program *make*.

```bash
sudo apt install make
```

If helmet or kubectl have not yet been installed, you can easily install them.

{{<tabs>}}
{{<tab "bash" "Ubuntu/Debian">}}make dependencies_ubuntu
{{</tab>}}

{{<tab "bash" "Fedora/CentOS">}}make dependencies_fedora
{{</tab>}}
{{</tabs>}}

*Note: Since Helm v3 no more Tillerserver is [required] on the sides of the Kubernet [https://helm.sh/blog/helm-3-released/).*

Now Kubectl must be configured so that a Kubernetes cluster can be accessed. (Use minikube for test purposes, otherwise ask the cluster administrator).

Afterwards the RDS ecosystem can be loaded onto the cluster with the following command:

```bash
make install
```

The above command installs all available services. Currently, the system does not yet check which services have been configured so that only these are set up. This currently means that unconfigured services will not work, but will be set up.

The system automatically installs a Jaeger instance for tracking log messages. You can access this instance with the following command and then call up the displayed IP address in the browser:

```bash
make jaeger
```

Jaeger is particularly well suited for identifying errors or problems within the ecosystem.

If a Prometheus system is used, all metrics are automatically tapped and offered in the respective system. A standardised view will be offered in the future (see [Issue 39](https://github.com/Sciebo-RDS/Sciebo-RDS/issues/39)).

---
title: Kubernetes
subtitle: Helm Chart und Installationsanleitung

menu:
  doc:
    parent: installation
weight: 302
---


You should follow the [configuration tutorial](/doc/getting-started/config/), before you can finish this tutorial.

There is a Makefile in the "deploy" folder, which is used via the program *make*.

```bash
sudo apt install make
```

If helm or kubectl have not yet been installed, you can easily install them.

{{<tabs>}}
{{<tab "bash" "Ubuntu/Debian">}}make dependencies_ubuntu
{{</tab>}}

{{<tab "bash" "Fedora/CentOS">}}make dependencies_fedora
{{</tab>}}

{{<tab "bash" "Windows 10">}}make dependencies_windows
{{</tab>}}
{{</tabs>}}

{{<callout "tip">}}
Note: Since Helm v3 no Tillerserver is [required](https://helm.sh/blog/helm-3-released/) on the Kubernetes side.
{{</callout>}}

Now kubectl must be configured so that a Kubernetes cluster can be accessed.

Afterwards the RDS ecosystem can be loaded onto the cluster with the following command:

{{<callout "warning">}}
The following command needs some configuration, which you made in the previous chapter. If you did not create the needed files, you will get a lot of error messages now. So be sure to follow the steps from the [configuration tutorial](/doc/getting-started/config/).
{{</callout>}}

```bash
make install
```

Now that the installation of the RDS instance is complete, a client software is now required. Currently the following plugins are available:

- [ownCloud Plugin](/doc/impl/plugins/owncloud/)

### Monitoring

The system automatically installs a Jaeger instance for tracking log messages. You can access this instance with the following command and then call up the displayed IP address in the browser:

```bash
make jaeger
```

Jaeger is particularly well suited for identifying errors or problems within the ecosystem.

If a Prometheus system is used, all metrics are automatically tapped and offered in the respective system. A standardised view will be offered in the future (see [Issue 39](https://github.com/Sciebo-RDS/Sciebo-RDS/issues/39)).

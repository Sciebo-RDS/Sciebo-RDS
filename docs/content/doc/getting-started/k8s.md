---
title: Kubernetes
subtitle: Helm Chart und Installationsanleitung

menu:
  doc:
    parent: installation
weight: 302
---

{{<callout "warning">}}
The commands in this chapter needs some configuration, which you made in the previous chapter. If you did not create the needed files, you will get a lot of error messages now. So please be sure to follow the steps from the [configuration tutorial](/doc/getting-started/config/).
{{</callout>}}

Now the RDS ecosystem can be loaded onto the cluster with the following command:

{{<tabs>}}
{{<tab "bash" "Install RDS">}}make install
{{</tab>}}

{{<tab "bash" "Uninstall RDS">}}make uninstall
{{</tab>}}
{{</tabs>}}

Now that the installation of the RDS instance is complete, a client software is now required. Currently the following plugins are available:

- [ownCloud Plugin](/doc/impl/plugins/owncloud/)

### Monitoring

The system automatically installs a Jaeger instance for tracking log messages. You can access this instance with the following command and then call up the displayed IP address in the browser:

```bash
make jaeger
```

Jaeger is particularly well suited for identifying errors or problems within the ecosystem.

If a Prometheus system is used, all metrics are automatically tapped and offered in the respective system. A standardised view will be offered in the future (see [Issue 39](https://github.com/Sciebo-RDS/Sciebo-RDS/issues/39)).

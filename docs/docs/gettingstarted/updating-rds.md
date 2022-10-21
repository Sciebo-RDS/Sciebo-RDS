---
sidebar_position: 4
id: updating
displayed_sidebar: gettingstartedSidebar
---

# Updating Sciebo RDS

## Updating Kubernetes
Updating Sciebo RDS is simple.

1. Update your helm package list:

```bash
helm repo up
```

2. Rerun the helm command from the previous step:

```bash
helm upgrade -i sciebords -f values.yaml sciebords/all
```

## Updating Owncloud

### Updating via Owncloud marketplace

Update the plugin through the marketplace as you update any other plugin.

### Updating manual installation from source

Follow the same procedure you used to [install the plugin from source](./ocplugin#installing-manually-from-source).
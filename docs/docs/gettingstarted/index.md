---
sidebar_position: 1
id: start
displayed_sidebar: gettingstartedSidebar
---

# Introduction

This walk-through will give you all the necessary steps to get a fully fledged Sciebo RDS instance up and running, including storage provider connection. OwnCloud is currently the only supported storage provider, support for Nextcloud is in the works. Meanwhile, it is possible to add support for other EFSS systems through your own means, as explained [here](./../documentation/development/contributing/developing-for-efss).

### Prerequisites

You will need:

1. A Kubernetes cluster
2. An OwnCloud instance
3. Two different domains

The first domain will be used for [Describo](https://github.com/Arkisto-Platform/describo-online), the embedded metadata editor, and the main Sciebo RDS interface, while the other domain will be used to integrate your storage provider. Please link the domains to your Kubernetes cluster. It is vital that you have two domains, they are required in all configuration steps. The domains have to be root level, sub domains are supported.
---
sidebar_position: 2
id: ocplugin
displayed_sidebar: gettingstartedSidebar
---

# ownCloud


Currently ownCloud is the only storage provider, we support. We wrote a custom ownCloud plugin, which you have to install in your instance. The ownCloud marketplace is a good place to go, but if you want to be really up to date you should take a look into our [release page](https://zivgitlab.uni-muenster.de/sciebo-rds/sciebo-rds/-/tags). There you can find [multiple tags](https://zivgitlab.uni-muenster.de/sciebo-rds/sciebo-rds/-/releases/v0.1.9), which have an `oc-rds-plugin.tar.gz` file. This file should be used in your pipelines. Please remember the used tag, because you will need it later.

Also we have a dependency for the oauth2 plugin in ownCloud. (Because of a bug, you need to install the following php-extensions: `php-gmp php-bcmath openssl`.)

# Configuration

After you place tthe plugins in your ownCloud instance and enabled it, you have to create an oauth client for `sciebords` (uncheck `allow subdomains`) which uses the domain for the sciebo rds ui as the `redirection url`. The given oauthname will be used in the sciebo rds admin section, which can be found left in your admin configuration page. 

![](/docs/oc-plugin-view-admin-oauth.png)

When you are done, go to the sciebo RDS admin page. There enter the domain for sciebo rds ui and the oauthname again.

![](/docs/oc-plugin-view-admin.png)

Now you will find the sciebo RDS app in the top left app menu inside of your ownCloud instance. But there will be an error, because the backend side is missing. This will be done in the next step.
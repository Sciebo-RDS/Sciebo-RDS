---
sidebar_position: 2
id: ocplugin
displayed_sidebar: gettingstartedSidebar
---

# Configuring Owncloud


To use Sciebo RDS with Owncloud, you will have to install the Sciebo RDS Owncloud plugin.

##### Dependencies

Our plugin depends on the oauth2 plugin for Owncloud, which you can install from the [marketplace](https://marketplace.owncloud.com/apps/oauth2). Because of a bug, you also need to install the following php-extensions:

    php-gmp
    php-bcmath
    openssl

## Installing the Plugin

You have the choice of either:

- Installing it via the Owncloud marketplace
- Installing from source, using our release page.



### Owncloud Marketplace installation

Install the [plugin](https://marketplace.owncloud.com/apps/rds) from the marketplace. This version will probably not be as up-to-date as the releases provided by our release page. 

### Installing manually from source
1. Download the latest [tag](https://zivgitlab.uni-muenster.de/sciebo-rds/sciebo-rds/-/tags) from our [release page](https://zivgitlab.uni-muenster.de/sciebo-rds/sciebo-rds/-/releases/).
You will need the `oc-rds-plugin.tar.gz` file. Please remember which version you download, this will become important later on.

2. Extract the tar ball into your apps folder and enable the app through the Owncloud interface.

You can read more on how to manually install Owncloud plugins in their [documentation](https://doc.owncloud.com/server/next/admin_manual/installation/apps_management_installation.html#installing-apps-manually).

## Configuration

1. Create an oauth2 client for `sciebords` (uncheck `allow subdomains`). Use your first Sciebo RDS domain as the `redirection url`. The given oauthname will be used in the sciebo rds admin section, which can be found on the left hand side of your admin configuration page. 

![](/docs/oc-plugin-view-admin-oauth.png)

---
2. Next, go to the Sciebo RDS admin page, which can be found on the left hand . Enter the domain domain you provided for the oauth2 client, and the oauthname.

![](/docs/oc-plugin-view-admin.png)

---
3. You will now find the Sciebo RDS app in the top left app menu inside your Owncloud instance. There will be an error, as the backend is not yet set up. This will be done in the next step.
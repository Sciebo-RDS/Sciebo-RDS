# Owncloud

## Plugin Installation

### via source

Please refer to the [Configuring Owncloud](../../../gettingstarted/ocplugin.md) page of our Getting Started guide to see how to install the plugin from source.

### via Marketplace

Install the [plugin](https://marketplace.owncloud.com/apps/rds) from the marketplace. This version will probably not be as up-to-date as the releases provided by our release page.

## Plugin Configuration

Please refer to the [Configuring Owncloud](../../../gettingstarted/ocplugin.md) page of our Getting Started guide to see how to configure the plugin via the admin UI.

### Commandline

You can use the `occ` command to configure the plugin without the need to use the admin UI.

````bash
$ occ rds
rds
  rds:create-keys                        Creates the private and public key to sign informations.
  rds:reset                              Resets values in owncloud config
  rds:set-oauthname                      Sets the name of oauth client used by RDS app.
  rds:set-url                            Sets the iframe url within RDS app.
````

will explain all commands related to the sciebo RDS plugin.
This command is very handy for automized setup scripts.

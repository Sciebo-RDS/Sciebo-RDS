---
title: "Deploy as an app in ownCloud 10"
date: 2018-05-02T00:00:00+00:00
weight: 1
geekdocRepo: https://github.com/owncloud/web
geekdocEditPath: edit/master/docs/deployments
geekdocFilePath: oc10-app.md
---

{{< toc >}}

The ownCloud Web is being deployed as an app to [ownCloud marketplace](https://marketplace.owncloud.com/) to enable easy early integration into existing ownCloud 10 instances.
After completing this setup, ownCloud Web will be available on `https://<your-owncloud-server>/index.php/apps/web`.

## Prerequisites
- Running [ownCloud 10 server](https://owncloud.com/download-server/) with version 10.6
- Installed [oauth2 app](https://marketplace.owncloud.com/apps/oauth2)
- Command line access to your server

## Deploying ownCloud Web
Download the [ownCloud Web app](https://marketplace.owncloud.com/apps/web) from the marketplace and enable it:
```console
occ market:install web
```

## Configure oauth2
Within the `Admin` page of ownCloud 10, head into `User Authentication` and add a new client with arbitrary name (e.g. `ownCloud Web`) and redirection URL `https://<your-owncloud-server>/index.php/apps/web/oidc-callback.html`.

{{< figure src="/clients/web/static/oauth2.jpg" alt="Example OAuth2 entry" >}}

## Configure ownCloud 10
### Set ownCloud Web address
To set the ownCloud Web address and to display ownCloud Web in the app switcher, add the following line into `config/config.php`:

```php
'web.baseUrl' => 'https://<your-owncloud-server>/index.php/apps/web',
```

### Configure link routing
Administrators can optionally decide whether ownCloud Links (public and private links) should be provided by the Classic web interface or by ownCloud Web using the `web.rewriteLinks` option in `config/config.php`. The option defaults to `false` so that the links open in the Classic web interface. Setting it to `true` will redirect all links to ownCloud Web. To redirect all private and public links to ownCloud Web, add the following line into `config/config.php`:

```php
'web.rewriteLinks' => true,
```

### Make ownCloud Web the default web interface
Administrators can optionally decide to make ownCloud Web the default web interface that users see after they log in to ownCloud. By default the Classic web interface will be presented to users. To present ownCloud Web to users by default, add the following line into `config/config.php`:

```php
'defaultapp' => 'web',
```

{{< hint info >}}
While it is possible to make ownCloud Web the default web interface, the decision should be carefully evaluated. Features are still being added to ownCloud Web and users might need to use the Classic web interface to do certain actions.
{{< /hint >}}

## Configure ownCloud Web
There are a few config values which need to be set in order for ownCloud Web to work correctly. Please copy the example config below into `config/config.json` and adjust it for your environment:

```json
{
  "server" : "https://<your-owncloud-server>",
  "theme": "owncloud",
  "auth": {
    "clientId": "<client-id-from-oauth2>",
    "url": "https://<your-owncloud-server>/index.php/apps/oauth2/api/v1/token",
    "authUrl": "https://<your-owncloud-server>/index.php/apps/oauth2/authorize"
  },
  "apps" : [
    "files",
    "media-viewer",
    "draw-io"
  ],
  "applications" : [
    {
      "title": {
        "en": "Classic Design",
        "de": "Dateien",
        "fr": "Fichiers",
        "zh_CN": "文件"
      },
      "icon": "switch_ui",
      "url": "https://<your-owncloud-server>/index.php/apps/files"
    },
    {
      "icon": "application",
      "menu": "user",
      "target": "_self",
      "title": {
        "de": "Einstellungen",
        "en": "Settings"
      },
      "url": "https://<your-owncloud-server>/index.php/settings/personal"
    }
  ]
}
```

|config parameter|explanation|
|---|---|
|server|ownCloud 10 server address|
|theme|Theme to be used in ownCloud Web pointing to a json file inside of `themes` folder|
|auth.clientId|Client ID received when adding ownCloud Web in the `User Authentication` section in `Admin`|
|apps|List of internal extensions to be loaded|
|applications|Additional apps and links to be displayed in the application switcher or in the user menu|
|applications[0].title|Visible title in the application switcher or user menu, localizable|
|applications[1].menu|Use `user` to move the menu item into the user menu. Defaults to app switcher|

{{< hint info >}}
It is important that you don't edit or place the `config.json` within the app folder. If you do, the integrity check of the app will fail and raise warnings.
{{< /hint >}}

## Accessing ownCloud Web
After following all the steps, you should see a new entry in the application switcher called `New Design` which points to the ownCloud web.

{{< figure src="/clients/web/static/application-switcher-oc10.jpg" alt="ownCloud 10 application switcher" >}}

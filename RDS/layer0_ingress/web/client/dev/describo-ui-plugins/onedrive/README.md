# describo-ui-plugins : onedrive

- [describo-ui-plugins : onedrive](#describo-ui-plugins--onedrive)
- [Dependencies](#dependencies)
  - [Using the plugin](#using-the-plugin)
    - [Register the plugin with vue](#register-the-plugin-with-vue)
    - [Store events](#store-events)
  - [Setting up Azure](#setting-up-azure)
    - [Register the application](#register-the-application)
    - [Authentication](#authentication)
      - [API permissions](#api-permissions)
    - [Get the configuration data](#get-the-configuration-data)
    - [Developer Documentation](#developer-documentation)

A plugin providing a component to authenticate to Microsoft Onedrive and produce an rclone
configuration for onedrive access.

The plugin has two components:

-   `onedrive-authenticator-component`
-   `onedrive-file-preview-component`

Usage:

```
<onedrive-authenticator-component />
```

And it registers one service: `this.onedriveAuthenticationManager`:

-   To get the account info of the user: `this.onedriveAuthenticationManager.getAccount()`
-   To get the current access token: `this.onedriveAuthenticationManager.getToken()`

# Dependencies

Install these dependencies in the app in which you use this plugin.

-   npm install --save "@azure/msal-browser"

## Using the plugin

### Register the plugin with vue

```
 Vue.use(OneDrivePlugin, {
    ...configuration.services.onedrive,
    log,
    configuration: "/session/configuration/onedrive",
});
```

In order to register the plugin you need to provide:

-   `the configuration from the app`: the UI gets any available application configuration from
    `ui.services.onedrive`
-   `log`: a logging function with log, debug, info, etc methods..
-   `$http`: a service that can perform http operations to your API. The service must expose:

-   a method `post` that takes two params: route and body

```

await $http.post({ route: this.config.configurationEndpoint, body: configuration, });

```

-   `configuration`: your API path to save configuration information for use in the backend (POST)

### Store events

This plugin will try to set the target resource in the store using:

```
this.$store.commit("setTargetResource", {
    resource: "owncloud",
});
```

## Setting up Azure

In order to use this plugin you firstly need to create a registration for this application. This
applies to both development and production.

Follow the documentation at
[https://docs.microsoft.com/en-us/azure/active-directory/develop/scenario-spa-app-registration](https://docs.microsoft.com/en-us/azure/active-directory/develop/scenario-spa-app-registration).
Specifically, follow the `MSAL.js 2.0 with auth code` flow docs.

### Register the application

-   Register an application
    -   name: `describo-online-onedrive`
    -   supported account types:
        `Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)`
    -   Redirect URI: `http://localhost:9000/onedrive-callback`

Ensure you setup a `Single-page application`.

### Authentication

After registering the application navigate to the `Authentication` tab (in the sidebar) and enable
`Access tokens` and `ID tokens` in the `Implicit grant` section.

#### API permissions

After registering the application navigate to the `API Permissions` tab (in the sidebar) and add the
following permissions:

-   Files.Read
-   Files.Read.All
-   Files.ReadWrite
-   Files.ReadWrite.All
-   offline_access
-   Sites.Read.All
-   User.Read

When you `Add a permission` you will be asked to choose an API. Select `Microsoft Graph`. Select
`Delegated permissions` then search for each permission and add it. Be sure to `save` when you're
done.

### Get the configuration data

You will need the `Application (client) ID` from the overview page and the `Redirect URI` from the
`Platform configurations` section of the `Authentication` tab.

### Developer Documentation

-   https://github.com/AzureAD/microsoft-authentication-library-for-js/tree/dev/lib/msal-browser

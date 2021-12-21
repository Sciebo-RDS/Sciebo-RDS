# describo-ui-plugins : onedrive

- [describo-ui-plugins : onedrive](#describo-ui-plugins--onedrive)
  - [Using the plugin](#using-the-plugin)
    - [Register the plugin with vue](#register-the-plugin-with-vue)
    - [Required configuration](#required-configuration)
    - [Store events](#store-events)
  - [Implementation information](#implementation-information)

A plugin providing components to authenticate to owncloud servers and preview content residing on
them.

The plugin has one component:

-   `owncloud-authenticator-component`

Usage:

```
<owncloud-authenticator-component />
```

And it registers one service: `this.owncloudAuthenticationManager`:

-   To get the account info of the user: `this.owncloudAuthenticationManager.getAccount()`

## Using the plugin

### Register the plugin with vue

```
    Vue.use(OwncloudPlugin, {
        router,
        log,
        $http: Vue.prototype.$http,
        configuration: "/session/configuration/owncloud",
        oauthToken: "/session/get-oauth-token/owncloud",
    });
```

In order to register the plugin you need to provide:

-   `router`: the vue router - the plugin will register an oauth callback at /owncloud-callback
-   `log`: a logging function with log, debug, info, etc methods..
-   `$http`: a service that can perform http operations to your API. The service must expose:
    -   a method `get` that takes one param: route

```
await $http.get({ route: this.config.configurationEndpoint })

```

-   a method `post` that takes two params: route and body

```

await $http.post({ route: this.config.configurationEndpoint, body: configuration, });

```

-   `configuration`: your API path from which to get the owncloud configuration (GET) and to save
    configuration to (POST)
-   `oauthToken`: your API path to post the oauth code to and kick off token retrieval from owncloud

### Required configuration

When the plugin does a `GET` to the endpoint defined by `configuration` it must return the following
information:

```
[
    {
        "name": "Test Owncloud",
        "url": "http://localhost:8000",
        "internalUrl": "http://owncloud_server:8080",
        "clientId": " your client id",
        "redirectUri": "http://localhost:9000/owncloud-callback",
        "oauthAuthoriseEndpoint": "/index.php/apps/oauth2/authorize",
        "oauthTokenEndpoint": "/index.php/apps/oauth2/api/v1/token",
        "webdavEndpoint": "/remote.php/dav"
    }
]
```

See the main documentation for configuring the application for more information on defining
services.

### Store events

This plugin will try to set the target resource in the store using:

```
this.$store.commit("setTargetResource", {
    resource: "owncloud",
});
```

## Implementation information

Owncloud implements an oauth login flow that uses both front end and back end hooks. In the front
end, the user is redirected to ownCloud to authorise application access. Then, if they do, ownCloud
redirects back to the application passing back a code that is then sent to `your` API. Your API must
then perform a POST to owncloud using the code and some configuration (see auth-manager.service.js:
getOauthToken for the details) in order to retrieve a token that lives for 1 hour.

This token is then sent back to `your` API for storage in the user session. An API service is
responsible for refreshing the token before it expires.

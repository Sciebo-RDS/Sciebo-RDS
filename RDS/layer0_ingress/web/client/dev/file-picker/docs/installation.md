---
title: "Installation"
date: 2020-08-26T10:56:03
weight: 3
geekdocRepo: https://github.com/owncloud/file-picker
geekdocEditPath: edit/master/docs
geekdocFilePath: installation.md
---

{{< toc >}}

## Setup authentication
The config for the server backend and authentication needs to be provided in json format. The full set of options is listed below in two examples. One for authentication with OAuth2 and one with OpenID Connect.  

There are different ways of providing the config JSON to the file picker:
- As a JSON object via a prop called `configObject`
- As a JSON string via the same prop (`configObject`)
- As a URL via a prop called `configLocation`. This requires full URL address (e.g. `https://<your-server>/<path-to-the-config>`)
- If none of the props (`configObject` or `configLocation`) is defined, the file picker has a `configLocation` of `https://<your-server>/file-picker-config.json` as fallback

Location of the file can be provided via a prop called `configLocation`. This requires full URL address (e.g. `https://<your-server>/<path-to-the-config>`). If the prop is not defined, the location will fallback to `https://<your-server>/file-picker-config.json`. The config can point to both oauth2 and OIDC. You can take a look at the following example to see how OIDC can be defined:

### OpenID Connect config
```json
{
  "server": "<owncloud-server>",
  "openIdConnect": {
    "metadata_url": "<your-server>/.well-known/openid-configuration",
    "authority": "<your-server>",
    "client_id": "<client-id>",
    "response_type": "code",
    "scope": "openid profile email"
  }
}
```

### OAuth2 config
```json
{
  "server": "<owncloud-server>",
  "auth": {
    "clientId": "<oauth2-client-id>",
    "url": "<your-server>/index.php/apps/oauth2/api/v1/token",
    "authUrl": "<your-server>/index.php/apps/oauth2/authorize"
  }
}
```

### Pass bearer token
In case you already have a bearer token and want to skip the whole authorization process inside of the File picker, you can pass it to the component via prop called `bearerToken`.

## Install File picker package
To integrate File picker into your own product, you can install it via one of the following commands:

```bash
npm install @ownclouders/file-picker --save
# OR
yarn add @ownclouders/file-picker
```

## Select browser storage
In order to authorize any request to the ownCloud server, we are storing the Bearer token in a browser storage. By default, it is the session storage. As browsers are adding more strict policies when it comes to blocking third party cookies, your users might experience issues with the token not being saved in the storage. For this reason, it is possible to specify a storage name in the config of File picker. To make it possible to run the File picker inside of an iframe, specify `storage: memory`.

{{< hint danger >}}
If the memory storage is used, it is not persisted in the session. This leads to users having to authorize again after a refresh has happened.
{{< /hint >}}

{{< hint info >}}
Users might still be experiencing issues with the authentication even if the memory storage is used. That can happen due to the authentication popup needing to trigger a callback in the File picker. To make sure it will work as supposed, be sure to set correct CORS headers.
{{< /hint >}}

## Integrate in HTML page with vanilla JavaScript
When including File picker in an HTML page, it is important to include Vue.js as well. In this case, we will import it via [unpkg](https://unpkg.com). Without this, the component won't work. Vue needs to be included also if you're importing the File picker into a web application built with other framework than Vue (e.g. React, Angular).

```html
...
<meta charset="utf-8">
<title>File picker example</title>
<script src="https://unpkg.com/vue"></script>
<script src="https://unpkg.com/file-picker/dist/wc/file-picker.js"></script>
...


<file-picker id="file-picker" variation="resource"></file-picker>
```

## Integrate in Vue web application
There is a caveat when using the File picker inside an existing Vue application. Since the web component will be imported before Vue, we need to define it as a global variable on our own.
This requires us to separate the import of Vue into a bootstrap file.

vue.js:
```js
import Vue from 'vue'
window.Vue = Vue
```

main.js:
```js
import Vue from './vue'

new Vue(...)
```

```vuejs
<template>
  <file-picker variation="location" />
</template>

<script>
import FilePicker from '@ownclouders/file-picker'
import '@ownclouders/file-picker/dist/lib/file-picker.css'

export default: {
  components: {
    FilePicker
  }
}
</script>
```

## Set correct variation
As described in [Getting Started]({{< ref "getting-started.md#components-of-the-file-picker" >}}), File picker comes in two variations. To define which one should be used, you need to pass it to the component via its `variation` property. Valid values are:
- `resource` - File picker
- `location` - Location picker

## Theming
File picker comes by default with extracted stylesheet which combines our ownCloud Design System and a few custom styles. If you want to create a custom theme, do not include our stylesheet and create a custom one using File picker selectors.

## Buttons and events
The wording of buttons can be customized.

### Select button
The file picker has a button in the top right for emitting an event with the selected location or resource, depending on the configured variation.
This button has default labels, depending on the chosen variation. However, it is possible to define a different button label by setting
`select-btn-label="<your select button label>"`. Using the select button will emit an event with the name `selectResources`.

### Cancel button
Cancellation for the file picker is disabled by default. When a label is provided, the file picker renders a cancel button on the left side of the select button.
This can be achieved by setting `cancel-btn-label="<your cancel button label>"`. This will also add a keyboard event on the `ESC` key. Using
the cancel button or the `ESC` key on the keyboard will emit an event with the name `cancel`.

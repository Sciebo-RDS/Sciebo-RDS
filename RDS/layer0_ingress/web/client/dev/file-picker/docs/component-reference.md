---
title: "Component reference"
weight: 6
geekdocRepo: https://github.com/owncloud/file-picker
geekdocEditPath: edit/master/docs
geekdocFilePath: component-reference.md
---

{{< toc >}}

```vuejs
<file-picker>
```

## Props
| Property | Type | Default | Description |
| :------- | :--- | :------ | :---------- |
| `variation` | `String` | | Specifies if File Picker (`resource`) or Location Picker (`location`) should be used |
| `configLocation` | `String` | `window.location.origin + '/file-picker-config.json'` | Defines where the config file should be located |
| `bearerToken` | `String` | `null` | Bearer token used for requests authentication. If specified, authorization step is skipped |
| `configObject` | `String | Object` | | File Picker config. If defined, fetching config from `configLocation` is skipped |
| `isSdkProvided` | `Boolean` | `false` | Asserts whether ownCloud SDK is already initialised in the consuming app |
| `selectBtnLabel` | `String` | `null` | Replaces the select button label |
| `isSelectBtnDisplayed` | `Boolean` | `true` | Asserts whether the select button should be displayed |
| `cancelBtnLabel` | `String` | `nulll` | Displays the cancel button and uses the given value as a label |
| `isOdsProvided` | `Boolean` | `false` | Asserts whether the ownCloud Design System has been already initialised in the consuming app |
| `locale` | `String` | `null` | Sets the language in which the File Picker should be displayed. If omitted, the browser language will be used |
| `isInitialFocusEnabled` | `Boolean` | `false` | Enables focusing last item of breadcrumbs after the first folder has been loaded |

## Events
| Event | Arguments | Description |
| :---- | :-------- | :---------- |
| `update` | Resources array | Emitted when any resource is selected or deselected or if a folder has been loaded in location picker |
| `select` | Resources array | Emitted when the select button is clicked |
| `cancel` | Native click event object | Emitted when the cancel button is clicked |
| `folderLoaded` | Current folder object | Emitted when loading of a folder has ended |
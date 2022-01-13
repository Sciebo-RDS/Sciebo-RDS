---
title: "Focus Management"
weight: 7
geekdocRepo: https://github.com/owncloud/file-picker
geekdocEditPath: edit/master/docs
geekdocFilePath: focus-management.md
---

{{< toc >}}

File Picker comes only with partial focus management. If you want to focus an element, it needs to be achieved through a code in the consuming app.

## Focusing content of File Picker
If you're including File Picker as a web component, managing focus is slightly different from focusing content of any other component in the DOM tree. Since web component are living in shadow root, we need to send the focus into it. To focus e.g. a checkbox within the File Picker, you can use the following code.

```js
document.querySelector('#file-picker').shadowRoot.querySelector('.oc-breadcrumb-list-item span[aria-current="page"]').focus()
```

{{< hint info >}}
The `#file-picker` selector is coming from the consuming app, not from File Picker.
{{< /hint >}}

## Initial folder load focus
After opening a folder, we are focusing the last item of breadcrumbs. This is not the case when loading the first folder. Any following navigation into the first folder will focus the item. To enable focus on the first load as well, you need to set `isInitialFocusEnabled` prop to `true`.
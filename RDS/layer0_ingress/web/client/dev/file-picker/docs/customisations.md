---
title: "Customising"
weight: 5
geekdocRepo: https://github.com/owncloud/file-picker
geekdocEditPath: edit/master/docs
geekdocFilePath: customising.md
---

{{< toc >}}

It is possible to customise certain parts of the File Picker with the help of props.

## Variation
File picker comes in two different variations - File Picker and Location Picker. To specify which one should be used, set property `variation` to `resource` or `location`.

### File Picker
File picker variation is used to select resources from within your ownCloud instace. It is possible to select multiple files and folders.

### Location Picker
Location picker variation is used to select location inside of your ownCloud instance. It is only possible to select one folder.

## Actions
If you do not wish to include the default File Picker actions (select and cancel), you can hide both of them.

### Select
Select resources/location button can be hidden by setting prop `isSelectBtnDisplayed` to `false`.

### Cancel
Hiding Cancel button slightly differes to the Select button. If you do not wish to display the cancel button, simply leave out any value for prop `cancelBtnLabel` and the component will be hidden by default.
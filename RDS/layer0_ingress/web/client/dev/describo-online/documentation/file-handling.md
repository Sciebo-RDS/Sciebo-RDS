# File handling in Describo

- [File handling in Describo](#file-handling-in-describo)
  - [UI](#ui)
  - [API](#api)
  - [File operations in describo](#file-operations-in-describo)
    - [list all in folder on `remote resource`](#list-all-in-folder-on-remote-resource)
    - [copy file from `remote resource` to `local store`](#copy-file-from-remote-resource-to-local-store)
    - [copy file from `local store` to `remote resource`.](#copy-file-from-local-store-to-remote-resource)
  - [Rclone Configuration](#rclone-configuration)
  - [Session Object](#session-object)

Describo only handles one file: `ro-crate-metadata.json`. This document will explain the code and
steps surrounding file selection.

## UI

When a user logs into describo and selects a backend to use they get a file browser to walk the
backend and pick a folder to work with. When they select a folder a post message is sent to the API
to load that folder. This happens in the UI code @ `src/components/LoadCollection.component.vue`.
The method `loadFolder` does a POST to `/load` with the following information:

```
{
    resource: 'onedrive' (or could be reva),
    folder: the selected folder to scan,
    id: the folder id (this is a onedrive thing but I expect owncloud will have something similar - that said, it might not be necessary when talking to owncloud)
}
```

## API

For the rest of this document:

-   `remote` or `remote resource` means the storage backend: onedrive, owncloud, whatever
-   `local store` means a folder on the describo API container. This folder is created as
    `/srv/tmp/${userId}` inside the container by the setup function in
    `api:src/lib/file-browser - setup`.

The post from the UI triggers the following set of events (this is in
`src/routes/load.js - loadRouteHandler`):

-   the folder on the remote resource (onedrive, reva, ...) is scanned for a file matching
    `ro-crate-metadata.{json,jsonld}` (json or jsonld)
    -   if there isn't one a new ro crate file is made in the describo API local store
    -   if there is more than one on the remote then an error is thrown as we don't know which one
        to use
    -   if there is only one in the remote resource then that file is copied from the remote back to
        the local store

When there is a ro-crate file in the `local store` (whether it's a brand new one or an existing
one):

-   if the ro crate file has a collection identifier in its header then describo looks for that
    collection id in the DB and continues with that.
-   if the ro crate file has a collection identifier in its header but that collection is not in the
    db a new collection is created in the db and the ro crate data is loaded into it
-   if the ro crate file does not have a collection identifier then one is created, the identifier
    is written into the ro crate file in the `local store` and then the ro crate file is copied back
    to the `remote resource`.

From this point on, all operations happen on the data in the DB. And, whenever that data changes,
the changes are walked and written into the ro crate file in the `local store` which is then copied
back to the `remote resource`.

## File operations in describo

### list all in folder on `remote resource`

File: src/lib/file-browser.js - listFolder

Requires `resource` and `folderPath`. Resource is used to get the required rclone configuration from
`session.data` which is injected by middleware into every request.

### copy file from `remote resource` to `local store`

File: src/lib/file-browser.js - syncRemoteFileToLocal

Requires: `resource`, `parent` and `name`. Parent is the path and name is the file to retrieve
(which in Describo's case will only be the ro crate file). The file is copied into the local store
working directory. Resource is used to get the required rclone configuration from `session.data`
which is injected by middleware into every request.

### copy file from `local store` to `remote resource`.

File: src/lib/file-browser.js - syncLocalFileToRemote

Requires: `resource`, `parent` and `localFile`. Parent is the path to sync the file to and localFile
is the file to sync back to the remote (which in Describo's case will only be the ro crate file).
The file is copied from the local store working directory. Resource is used to get the required
rclone configuration from `session.data` which is injected by middleware into every request.

## Rclone Configuration

File: src/lib/file-browser.js - writeRcloneConfiguration

The rclone configuration is written to disk during the setup stage of any file handling operation.
The configuration in that method is for onedrive but it's likely very similar to what is required to
talk to a webdav endpoint coming from owncloud or other cloud services.

## Session Object

Every user has a session object where you can store json data for user in other parts of the app.
The session object is made available on every request at `req.session.data`. So, this is where you
can store tokens or other information for backend services for use in file handlers and such.

Have a look at `src/routes/onedrive` for how the onedrive information is stored.

# Monorepo

We use a monorepo to make it easier to track related changes. This means that you will find all relevant files in a single [Github repository](https://github.com/Sciebo-RDS/Sciebo-RDS).

The following table will give an impression of the individual parts.  

| Folder           | Description                          |
| ---------------- | ------------------------------------ |
| /charts          | Helm charts                          |
| /docs            | Website with documentation           |
| /getting-started | Files for easy deployment            |
| /RDS             | The code for the connector services. |
| /                | Metafiles and configuration          |

If you want to contribute, follow this structure.

There is also an [additional repository](https://github.com/Sciebo-RDS/RDS-Connectors) that functions as a community hub for development of 3rd party connectors, such as Dataverse. These connectors are community managed – if you are planning on developing a connector and sharing it as Open Source, this is the place to do so.
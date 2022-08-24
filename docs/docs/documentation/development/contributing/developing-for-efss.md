# Developing an EFSS plugin

Currently, if you are implementing a new service in layer 2 or 3, it is necessary to create your own plugins or adapt an existing one, as they currently have no automation to integrate the new endpoints. All available plugins can be found in the Git repository. The services in layer 1, called the Port Service, are automatically provided by the Token Storage, connected to the Research Manager, and used by the Metadata and Exporter Service.

Select a plugin (Example: Owncloud) and see the integration. (Owncloud itself offers a Developer Manual.)
# Developing an EFSS plugin

When implementing a new service for Layer 2 or 3, you have to create your own plugin or adapt an existing one. All available plugins can be found in the Git repository. The services in Layer 1 (the ports layer) are automatically provided tokens by the token storage, which is connected to the Research Manager and used by the Metadata and Exporter Service.

Take a look at the Owncloud plugin to see how the integration into other EFSS systems might be implemented. You should also refer to the developer manual of your EFSS to learn how to develop a Plugin.
---
title: Token Storage
subtitle: Give this service your secrets

menu:
  doc:
    parent: core
weight: 800
mermaid: true
---

# Introduction

This service provides secure handling and exchange of passwords and other access tokens.

## Encryption

Because of the high security in RDS, the communication between the plugins and the RDS system must be encrypted or at least signed. Since an OAuth2 provider is required for authentication, a client secret is passed from the provider to the RDS system at the very beginning of the configuration. This secret is used as a password to encrypt further communication between the two systems.

If this password is corrupted, an attacker can set up his own system and pretend to be an RDS system and thus carry out a man-in-the-middle attack, whereby all communication between the provider and the RDS system is broken, despite encryption. For this reason the OAuth2-Secret can be used as a key. If we cannot trust this secret, the entire communication is not secure (even without this secret as a key for synchronous encryption).

``mermaid
sequenceDiagram
  participant user
  participant RDS
  participant provider

  User ->> RDS: 1st login by provider
  RDS -->> User: 2nd Redirect Provider Login
  User ->> Provider: 3rd login successful
  Provider -->> RDS: 4. user data forwarding
  Provider -->> User: 5th Redirect RDS Logged-In
```

Because of the secrecy of the Oauth2-secret, all plugin communication must be routed through a server structure that has access to this secret. This must then be behind a login page, so that the user must be authenticated. So RDS can be sure that the request is authorized by the user, because we trust the plugin system. If we can't do this, the OAuth2 provider is not trustworthy either, because an attacker can impersonate another person, and OAuth2 would lose its trust.

## UML Diagram

Due to the high relevance of a faultless storage of the user tokens, a UML diagram with cardinalities describing the storage structure of the data is presented in the following.

``mermaid
classDiagram

  class Storage {
    - List [Token value] _storage
    - List [User value] _user
    - List [Service value] _service
  }

  class User {
    + string username
    + String userpassword
    + String loginservice
  }

  class Service {
    + String service name
    + String client_id
    + String client_secret
    + String authorize_url
    + String refresh_url
  }

  class token {
    + string username
    + String service name
    + String access_token
    + String refresh_token
    + datetime expiration_date
  }

  Storage "1" -- "0..n" Token : has
  Storage "1" -- "0..n" User : has
  Storage "1" -- "0..n" Service : has

  Token "0..n" -- "1" Service : has
  Token "0..n" -- "1" User : has
```

Currently, each user can only have one token for each service. This is currently ensured by the fact that tokens are already identical if their service names match.

## Schedules

Due to the easier handling, the data is currently only stored in the memory. This means that as soon as the service is interrupted, all data is also lost, which means that all users have to log in again. In the future, this will be remedied by persistent and cross-cluster storage.

# OpenAPI v3

{{< swagger-spec url="https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle3_central_services/token_storage/central-service_token-storage.yml"  >}}

{{% code file="doc/impl/central/token-storage-docstring.md" %}}

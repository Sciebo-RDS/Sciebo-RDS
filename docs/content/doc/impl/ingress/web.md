---
title: RDS Web
subtitle: The frontend service

menu:
  doc:
    parent: ingress
weight: 800
mermaid: true
---

# Introduction

This service provides the entrypoint to sciebo RDS, so it provides the user frontend. The user frontend can be used standalone or integrated into other interfaces with an iframe. Also it handles the communication between the backend and the frontend via socket.io with the help of vuex stores. So the backend can send data to the frontend without the need of interactions from the user.

The integration of the frontend is handled by the plugins.

# Sequences

In the following you can see how some important flows are working.

## User provider login

```mermaid
sequenceDiagram
    participant U as User
    participant F as RDS-Web
    participant B as Backend
    U->>F: Requests login status
    opt not logged in
        U->>F: Logs user in without sciebo RDS account
    end
    U->>F: Requests available service informations 
    F-->>B: Pulls all needed informations
    F-->>U: Send service informations. Stored in vuex
    U->>U: Open needed oauth2 service link
    U->>F: Redirected by the oauth2 workflow with valid exchange code
    F-->>B: Create sciebo RDS account with tokens
    F->>U: Send user service informations
```

## User oauth2 authentication 

Mainly the same as provider login except the login stuff, because the user is already logged in with valid provider<->sciebo RDS connection.

## Research creation and update

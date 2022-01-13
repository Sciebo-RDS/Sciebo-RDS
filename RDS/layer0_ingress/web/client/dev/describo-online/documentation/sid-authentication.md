# Documentation about the SessionID (sid) authentication flow

- [Documentation about the SessionID (sid) authentication flow](#documentation-about-the-sessionid-sid-authentication-flow)
  - [External Service](#external-service)
  - [On the UI](#on-the-ui)
    - [Checking a user is known and protecting routes.](#checking-a-user-is-known-and-protecting-routes)
  - [Logging in a user](#logging-in-a-user)
  - [On the API](#on-the-api)
    - [api:/authenticated and demandKnownUser middleware](#apiauthenticated-and-demandknownuser-middleware)
            In this flow some external service has already authenticated a user and wishes to set up a session
            in describo for them to use.

## External Service

The external service is expected to POST to describo `api:/session/application` which extracts the
`authorization` header looking for `bearer` and taking the token. That is passed to `@/lib/session/postSession`
which checks that token against the configuration for the api to ensure that the calling application is
authorised to use this endpoint.

If it is it creates the user session and returns the `session id` from the DB table.

The external application can then load an iframe with a URL like `${describo online}/application?sid=${session id}

## On the UI

### Checking a user is known and protecting routes.

This is the same as documented in [Checking a user is known and protecting route](./okta-authentication#Checking-a-user-is-known-and-protecting-routes)

## Logging in a user

If the UI is loaded with `/application?sid=...` in the URL the component
`@components/ApplicationLogin.component` is loaded. This component extracts the SID in the URL and
sets it in session storage via `auth-service/setSessionID`.

At this point the user is logged in.

## On the API

### api:/authenticated and demandKnownUser middleware

This is the same as documented in [api:/authenticated and demandKnownUser middleware](./okta-authentication#api:/authenticated-and-demandKnownUser-middleware)

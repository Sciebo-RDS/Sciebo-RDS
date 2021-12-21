# Documentation about the okta authentication flow

- [Documentation about the okta authentication flow](#documentation-about-the-okta-authentication-flow)
  - [On the UI](#on-the-ui)
    - [Checking a user is known and protecting routes.](#checking-a-user-is-known-and-protecting-routes)
    - [Logging in a user](#logging-in-a-user)
  - [On the API](#on-the-api)
    - [api:/authenticated and demandKnownUser middleware](#apiauthenticated-and-demandknownuser-middleware)
    - [api:/session/okta](#apisessionokta)

Okta is used to handle usernames and passwords in this app. The API does not see the user's password
as the authentication happens in the UI in the users' browser.

## On the UI

### Checking a user is known and protecting routes.

The check for whether the user is known happens in `src/routes.js` in the method `onAuthRequired`.
This method is run for all route changes.

In that method if the user is navigating to a route with `meta: { requiresAuth }`
then `authService-isAuthenticated` is run to check whether the user is known. That method peforms a
GET to `api:/authenticated` with a header set to either:

-   `authorization: sid ${some id}`
-   `authorization: okta ${some JWT from okta}`

The headers for all requests are set in `http.service-getHeaders`.

### Logging in a user

If the user is not logged in as determined by the check above then they will be sent to the `/login` route
with the `@/components/OktaLogin.component` component.

This component sets up the okta signin widget and the user talks to Okta directly with this. If the user
signs in, okta will redirect them back to the `/okta-login` route which has
`@/components/OktaLoginCallback.component`. This component uses the okta tools to store the auth token (JWT)
in session storage before submitting a POST to `api:/session/okta` with the user's email and name to
set up an account for the user. Importantly, this POST has an authorisation header with the okta token
from session storage.

## On the API

### api:/authenticated and demandKnownUser middleware

This route endpoint does nothing. But it does pass through the `demandKnownUser` middleware which checks
whether the user is known / authorised and continues or rejects the request. The middleware is in
`@/middleware`.

`demandKnownUser`:

-   fails with 401 if no authorization header in request
-   fails with 401 if authorization header present but doesn't match `okta` or `sid`
-   if auth header present with `okta` or `sid` token a lookup is performed on the `session` table in the DB to see whether the session is valid and the user should be allowed through
    -   If session found but expired then it's get deleted from DB and user gets 401
    -   If no session found user gets 401
    -   If session found and is still active the user info and session info is stored in the request object for all downstream route handlers (req.user and req.session)

### api:/session/okta

When the UI handles the callback from okta if everything is ok it POSTS to this endpoint which extracts the token from the authorization header and uses the Okta libs to verify that the token is ok
(`@/routes/index/createOktaSession`).

That okta libs necessarily involve a check of the okta JWT with okta which is quite slow (about a second) so if the token is good, a session is created for the user in the local DB so all future requests
don't need to call out to okta each time. The data in the session table is just the data in the token
unpacked (along with the token just in case).

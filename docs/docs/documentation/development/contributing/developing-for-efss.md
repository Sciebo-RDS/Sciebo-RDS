# Developing an EFSS Plugin

This part will show you how to integrate sciebo RDS into your own EFSS, if there is no plugin for your EFSS software.
Sciebo RDS requires three separate communication links to your target EFSS, starting with the serverside of your EFSS. This will be the first link Sciebo RDS will utilize.

## Serverside EFSS Plugin

1. Generate a RSA-Key-Pair. We require HMAC-SHA256 to ensure high security.

2. Publish the public key of that pair to the `publickey` endpoint. Sciebo RDS will use the public key to validate JWT formated user data. This allows for clientside communication without any further authentication and reduces workload a lot.

The JWT Tokens needs to contain the following:

| fieldname | type     | description                                                                                 |
| --------- | -------- | ------------------------------------------------------------------------------------------- |
| "email"   | `String` | The user email address.                                                                     |
| "UID"     | `String` | The unique userId.                                                                          |
| "cloudID" | `String` | The user cloudId. This is the unique userId in the OCM. Also referred to as "federated ID". |

These values have be encoded as JWT `RS256` or `HMAC-SHA256` and signed with the generated private key from the first step.

The following HTTP-endpoints are required by the Sciebo RDS backend and have to be implemented by your Plugin.

| endpoint      | request params | response params                                                                                                                           | description                                                                                    |
| ------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| /publickey    | `{}`           | `{"publickey": "<jwt-public-key-for-verification>"}`                                                                                      | This endpoint only publishes the public key for verification.                                  |
| /informations | `{}`           | `{"jwt":"<jwt-signed-with-private-key>", "cloudURL": "<url to your efss with protocol>", "serverName": "<your domain without protocol>"}` | This endpoint will be requested by the users themselves and redirect the output to sciebo RDS. |

The `/informations` workflow enables sciebo RDS to get user information that is required for multi-tenant functionality. Otherwise, the oauth2 key would be required earlier in the process to get user information, which is not possible in all EFSS.

The next section will adress how to integrate Sciebo RDS.

## Clientside

We assume that your EFSS uses an UI composed of javascript and html.
The user interface of your Plugin needs to embedd sciebo RDS as an html iFrame. We recommend using the builtin configuration management tools of your EFSS UI to manage the URL for the iFrame. This will make adminstration less of a hassle.
The sciebo RDS interface uses the [`window.postMessage`](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage) function of the JavaScript standard library to communicate with the parent `window` object. This is where your EFSS UI and your Plugin live. You need to implement different [window.addEventListener](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener)s on the Plugin side to react to different events emitted by the iframe:

| eventname        | data | description                                                                                                             |
| ---------------- | ---- | ----------------------------------------------------------------------------------------------------------------------- |
| `init`           | `{}` | Emitted when Sciebo RDS is ready to get (serverside) user information directly from the user.                           |
| `showFilePicker` | `{}` | Emitted when the user wants to select a folder within your EFSS. This event should trigger the builtin EFSS filepicker. |


The Sciebo RDS UI can now talk to the EFSS UI and will get all relevant information from your EFSS without the need to communicate directly to your EFSS. You now need a connector to request files from your EFSS, which will be the next step.

## Connector

Now you have to integrate your EFSS into Sciebo RDS. This requires a filestorage connector, which is discussed on the [Developing Connectors](/documentation/development/contributing/developing-connectors) page.

## Wrap up

Now is the time to create a Dockerfile for your filestorage connector. Please refer to the Docker documentation to learn about dockerization. Next, create a Kubernetes manifest for the container - we highly recommend using Helm charts. Again, please refer to the corresponding documentation if you are not sure how to do this.
<!-- Now you can spin up your connector to connect sciebo RDS with your efss storage, place your server- and clientside code into your efss ui and you are ready to go. -->
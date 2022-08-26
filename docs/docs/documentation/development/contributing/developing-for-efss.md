# Developing an EFSS plugin

Now, you will learn how to integrate sciebo RDS into your own EFSS.
Because of the complex workflow, you need to establish three separate links between sciebo RDS and your target EFSS. We start with the serverside of your efss, because it is also the first sciebo RDS needs to communicate with.

## Serverside plugin inside of your efss

Security is a high value, so at first you need to generate a RSA-Key-Pair with HMAC-SHA256 and publish the public key under a separate endpoint. The public key is needed, because Sciebo RDS will verify all user informations which are in the JWT format, given by the user themselves, if it is valid. With this workflow, it is possible to use the user session on the clientside to communicate with sciebo RDS. This reduces the work alot.

The jwt needs to contain the following informations:

| fieldname | type     | description                                                                              |
| --------- | -------- | ---------------------------------------------------------------------------------------- |
| "email"   | `String` | The user email address.                                                                  |
| "UID"     | `String` | The unique userId.                                                                       |
| "cloudID" | `String` | The user cloudId. This is the unique userId in the OCM. Sometimes called "federated ID". |

Encode this informations as a dict / object / HashMap and encode it as JWT `RS256` or `HMAC-SHA256` and sign it with the generated private key.

The following HTTP-endpoints are required by sciebo RDS backend.

| endpoint      | request params | response params                                                                                                                           | description                                                                                    |
| ------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| /publickey    | `{}`           | `{"publickey": "<jwt-public-key-for-verification>"}`                                                                                      | This endpoint only publishes the public key for verification.                                  |
| /informations | `{}`           | `{"jwt":"<jwt-signed-with-private-key>", "cloudURL": "<url to your efss with protocol>", "serverName": "<your domain without protocol>"}` | Thir endpoint will be requested by the users themselves and redirect the output to sciebo RDS. |

The workflow with `/informations` enables sciebo RDS to get user informations it needs to achieve its multi-tenant functionality. Without this, the oauth key needs to be earlier in the process and will be used to get user informations, which is not always possible in all efss.

To integrate sciebo RDS, continue on clientside.

## Clientside

We assume, that your efss has an ui built with javascript and html.
The user interface should integrate sciebo RDS with a html iFrame. So the sciebo RDS interface can communicate with the efss builtin tools with `window.postMessage` function. So you need to implement different listeners on your `window` object to react on such events:

| eventname        | data | description                                                                                                                                    |
| ---------------- | ---- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `init`           | `{}` | Sciebo RDS emit this event, if it is ready to get the user informations directly from the user. This are the informations from the serverside. |
| `showFilePicker` | `{}` | Sciebo RDS emit this event, if the user wants to select a folder within your efss. This event should open the builtin filepicker.              |

To manage the url for the iframe, we recommend to use builtin tools for configuration management of your efss ui to get a much nicer administration experience.

Now, sciebo RDS UI can communicate with your efss ui and gets all relevant informations from your efss without the need to communicate directly to your efss. To request files from your efss, you need a connector, which will come next.

## Connector

Now, you have to integrate your efss into sciebo RDS. For this purpose, you need a filestorage connector. This is very equally to connect other repositories, so please follow the instructions on [this page](/documentation/development/contributing/developing-connectors).

## Conclusion

After you implement the filestorage connector for your efss, you should create a dockerfile, which places all files into one container. Then create the needed kubernetes manifests, for this purpore we highly recommend the use helm charts.Now you can spin up your connector to connect sciebo RDS with your efss storage, place your server- and clientside code into your efss ui and you are ready to go.

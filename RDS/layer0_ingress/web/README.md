# rds-web

The application to get RDS into the new OC Web, the old OC Classic and a standalone interface.

_This application currently only supports the classic backend, which is written in php. Not the ocis backend in golang!_

## Production Setup

```
make
docker
docker-compose
git
```

First you have to checkout this repository.
(Currently, most packages are not published as containers in dockerhub, because they are in a work-in-progress state.)

```bash
git checkout https://github.com/Sciebo-RDS/RDS-Web.git
cd RDS-Web
git submodule update --init --recursive
```

### Configuration

Notice: This installs an instance for owncloud `classic` and the new interface `web`. If you do not want this, you need to make the changes on your own.

You need to adjust the following configuration files:

- /.env
- /setup/web.config.json
- /setup/production-configuration.json

If you do not find this files in your folder, you have to cp the example files, which are placed next to the mentioned files.
For example, you have to do this:

```bash
cp .env.example .env
cp setup/web.config.json.example setup/web.config.json
cp setup/production-configuration.json.example setup/production-configuration.json
```

Notice: If you need to adjust the nginx configuration, please change the `setup/misc/nginx/nginx.edge.conf` file to your needs. All `.env` envvar`s are described further down this README.

While you configure all files, you will need oauth2 informations from ownCloud for the `web` interface. You could generate them by yourself to set them with force. This is the most convenient way: You need 2 tokens with only letters and a length of 64 from your favourite password generator.

But you can do it the long way: First you need to start the ownCloud instance (or open up your already running one) and activate oauth2 app. Then you can generate the oauth2 informations for a new .

```bash
docker-compose -f setup/docker-compose.yml --env-file .env up -d owncloud
@docker exec -it owncloud_server /bin/bash -c "occ market:install oauth2 && occ market:install web && occ app:enable oauth2"
```

Now open your browser and open the owncloud, which should be `http://localhost/index.php/settings/admin?sectionid=authentication`. The name does not matter, but the redirect url have to be `http://localhost/web/oidc-callback.html`.

If you want to change the domain, you need to setup `OWNCLOUD_DOMAIN` in `.env` file before you start up the owncloud instance.

Now you have all informations you need for the files.

For `describo-online` configuration, please take a look [here](https://github.com/Arkisto-Platform/describo-online). Notice, that the `secret` value in `production-configuration.json` needs to be equal with envvar `DESCRIBO_API_SECRET` in file `.env`.
For `oc-Web` you find the documentation [here](https://owncloud.dev/clients/web/deployments/oc10-app/).

## Development Setup

If you want to develope for this software, you do not want to restart docker container everytime you change something. For a better developer experience, we choose a different approach to setup.

### Dependencies

This application needs different software for different integrations.

For all, you need:

```
make
tmux
git
```

For the server backend (owncloud classic and rds), you need:

```
pipenv
[docker](https://docs.docker.com/get-docker/)
[php composer](https://getcomposer.org/download/)
```

_Docker-compose file can be found in `/client/dev/docker-compose.yml`._
_Composer package file can be found in `/client/packages/classic/php/composer.json`._

For webfrontend, you need:

```
npm lts
yarn
gettext
```

Best option for npm is [nvm](https://github.com/nvm-sh/nvm#install--update-script) `nvm install --lts`)
Yarn is needed, because of the workspace feature `npm install yarn`.
All nodejs dependencies can be installed through `yarn --cwd client install`.

### Notice

In `/client/dev/ocis` you can find the sourcecode for ocis. Currently, we do not develope our software for this backend, so we only use the owncloud classic backend. But for further development, this sourcecode will be needed. For this software, we will need the following software:

```
[golang](https://golang.org/dl/)
```

Run `git submodule update --init --recursive` to pull ocis and web servercode.

### Steps for development environment

If you use ubuntu, you can use for some dependencies `make install` in root.
Otherwise, please follow the steps.

#### Notices

First, you should think about, what you want to develope. You have the choice of:

- standalone
- owncloud classic
- owncloud web

`standalone` means, you will be redirected to an oauth server, which handles the login and redirects back, so the user only sees the RDS App in whole. The application does not have any access to informations about the user except the oauth2 access token. This problem will be handled through the rds backend server.

`owncloud classic` means, that the old frontend of owncloud will be used for integration. This is the easierst form of integration, because the standalone app can be loaded and initialized in the same context as the user runs the frontend. Here we will use a jwt for authentication, which will be evaluated on the rds server side.

`owncloud web` is the new standard of owncloud, which implements all extension in vue. This comes with a lot of new problems, so we handle this with an iframe. The communication between the 2 separate windows will be through the event bus of the browser. Here we will use a jwt for authentication, too.

If you have make your choice (you can also choose all three, but then you have to make all steps for e.g. you have to generate 2 clients in your oauth server).

#### Ports

In the following sections, you read a lot about ports. Here you have an overview, which port comes from which service.

| Port | Description                                                                            |
| ---- | -------------------------------------------------------------------------------------- |
| 8000 | Owncloud classic                                                                       |
| 8080 | Python Backend Server, which manages login for websocket and proxy for vue dev server. |
| 8082 | OC Web extension vue dev server, which manages the integration of RDS into OC Web.     |
| 8085 | Vue dev Server for RDS Standalone App                                                  |
| 8100 | Vue dev Server for Describo Standalone App                                             |
| 9100 | new owncloud web vue dev server                                                        |
| 9200 | ocis frontend, which proxies requests to port 9100 (currently not used)                |

### Configuration

We use the dotenv mechanic to provide a simple interface for configuration, which is compatible with the environment workflow of docker and kubernetes. So please configure the .env file to your needs.

```bash
cp .env.example .env
vi .env
```

| fieldname                           | description                                                                                                                                                                                                             | default                                                                                              |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| OWNCLOUD_URL                        | The url to your owncloud instance.                                                                                                                                                                                      | http://localhost:8000                                                                                |
| OWNCLOUD_OAUTH_CLIENT_ID            | The client identifier from your oauth2 provider.                                                                                                                                                                        | ABC                                                                                                  |
| OWNCLOUD_OAUTH_CLIENT_SECRET        | The client secret from your oauth2 provider.                                                                                                                                                                            | XYZ                                                                                                  |
| OWNCLOUD_OAUTH_CLIENT_REDIRECT      | The client redirect url from your oauth2 provider.                                                                                                                                                                      |                                                                                                      |
| EMBED_MODE                          | Set this to True, if you want to use the app in embed mode. False means standalone mode.                                                                                                                                | True                                                                                                 |
| RDS_INSTALLATION_DOMAIN             | Set this URL to your RDS backend installation. If this is not available for server, you will get authentication errors.                                                                                                 | http://localhost:9900                                                                                |
| FLASK_ORIGINS                       | Set here all origins from requests can come. Otherwise it will be rejected through CORS.                                                                                                                                | ["http://localhost:8080", "http://localhost:8085", "http://localhost:8000", "http://localhost:9100"] |
| OWNCLOUD_OAUTH_CLIENT_REDIRECT      | Set this URL for redirection on serverside through http statuscode 302. This needs to be the value, which you specify on your oauth2 provider side.                                                                     | http://localhost:8080                                                                                |
| VUE_APP_DESCRIBO_URL                | Set this URL for your describo instance.                                                                                                                                                                                | http://localhost:8100                                                                                |
| VUE_APP_FRONTENDHOST                | Set this URL to your frontend host.                                                                                                                                                                                     | http://localhost:8080                                                                                |
| VUE_APP_SOCKETIO_HOST               | Set this URL to your socketio host. In this implementation, it is the same as frontendhost.                                                                                                                             | http://localhost:8080                                                                                |
| DEV_WEBPACK_DEV_SERVER_HOST         | Set this URL to your vue app host, so the frontend host can proxy requests.                                                                                                                                             | "http://localhost:8085"                                                                              |
| VERIFY_SSL                          | Set this to `True`, if you want to verify ssl certs. `False` if you do not want that.                                                                                                                                   | `False`                                                                                              |
| DEV_FLASK_DEBUG                     | Set this to `True`, if you want more debug informations in console.                                                                                                                                                     | `True`                                                                                               |
| DEV_USE_PROXY                       | Set this to `True`, if you want to use the server as a proxy for vue app. _Only for development use, not for production!_                                                                                               | `True`                                                                                               |
| DEV_USE_PREDEFINED_USER             | Set this to `True`, if you want to use a predefined user. _Only for development use, not for production!_                                                                                                               | `False`                                                                                              |
| DEV_FLASK_USERID                    | Set the userId, which should be used, when `DEV_USE_PREDEFINED_USER` is `True`.                                                                                                                                         | test                                                                                                 |
| SECRET_KEY                          | This env var can be set, if you want to reuse flask encrypted data after a server restart. Otherwise it will generate everytime a new secret, which cannot be used do decrypt the informations of a previous execution. | ""                                                                                                   |
| OWNCLOUD_OAUTH_CLIENT_AUTHORIZE_URL | The authorize url for owncloud, so sciebo-rds can you redirect to it for authorization.                                                                                                                                 | http://localhost/apps/oauth2/authorize                                                               |
| DESCRIBO_API_ENDPOINT               | The describo api endpoint to create a session from rds backend.                                                                                                                                                         | http://localhost:9000/api/session/application                                                        |
| DESCRIBO_API_SECRET                 | The describo secret, which was specified in `production-configuration.json`, so sciebo-rds can authenticated against describo.                                                                                          | IAMSECRET                                                                                            |
| OWNCLOUD_VERSION                    | The owncloud version which will be setup.                                                                                                                                                                               | 10.7                                                                                                 |
| OWNCLOUD_DOMAIN                     | The owncloud domain                                                                                                                                                                                                     | localhost                                                                                            |
| HTTP_PORT                           | The owncloud port                                                                                                                                                                                                       | 8000                                                                                                 |
| ADMIN_USERNAME                      | The owncloud admin accountname.                                                                                                                                                                                         | admin                                                                                                |
| ADMIN_PASSWORD                      | The owncloud admin password.                                                                                                                                                                                            | admin                                                                                                |
| ADMIN_MAIL                          | The owncloud admin mailaddress.                                                                                                                                                                                         | not@valid.tld                                                                                        |
| SOCKETIO_HOST                       | The socketio host for sciebo-rds.                                                                                                                                                                                       | http://localhost                                                                                     |
| SOCKETIO_PATH                       | The socketio path for sciebo-rds.                                                                                                                                                                                       | /rds/socket.io                                                                                       |
| RDS_URL                             | The url for sciebo-rds to load it in iframe                                                                                                                                                                             | http://localhost:80/rds                                                                              |

The `REDIRECTION_URL` and `OWNCLOUD_OAUTH_CLIENT_SECRET` fields can only be set up correctly, when you start up the corresponding oauth backend before. So you have to start the backends and configure the `.env` file properly. After this, you can stop everything and can use the receipts in the corresponding sections for use.

For easier access, you should start only the owncloud backend with the following commands and enable the `oauth2` and `rds` app and add a new oauth2 path in the settings, which is described [here](https://doc.owncloud.com/server/admin_manual/installation/apps_management_installation.html), [here](https://doc.owncloud.com/server/admin_manual/configuration/server/security/oauth2.html#installation) and [here](https://www.research-data-services.org/doc/impl/plugins/owncloud/).

```bash
docker-compose -f client/dev/docker-compose.yml up -d
```

Now open the url `http://localhost:8000` in your favourite browser and enable and setup all needed apps. For oauth, you will need one client for domain `http://localhost:9100/oidc-callback.html`, when you want to develope for OC Web. If you want to develope for standalone, you will need a client for domain `localhost:8080`.
After this, you have all informations to configure the `.env` correctly. Now, you can continue with the setup.

Remind: If you delete all docker-resources (e.g. with `docker system prune --volumes`), you have to do all steps before again to get valid values for `.env` file.

### Client setup

Install all nodejs dependencies.

```bash
yarn --cwd client install
yarn --cwd client/dev/web install
```

Now, you have to configure the OC Web server

```bash
cp client/dev/web/config/config.json.sample-oc10 client/dev/web/config/config.json
vi client/dev/web/config/config.json
```

In the `config.json`, you have to specify your owncloud classic backend (in docker-compose specified with `localhost:8000`, you access it before in your browser) and set your clientId, which you generate previously in oauth2 app inside of your owncloud classic instance. This is also described [here](https://owncloud.dev/clients/web/backend-oc10/). When you want to change the config.php of the owncloud classic backend, you can get this done with `docker exec -it dev_owncloud_1 /bin/bash -c vi config/config.php`.

Beware: You have to change the port from `8080` to `8000` in the fields `url` and `authUrl`.
Then, you have to add our RDS application in `external_apps` field. Copy the following code snippet and add it to the array.

```javascript
{
    "id": "rds",
    "path": "http://localhost:8082/index.js",
    "config": {
        "url": "http://localhost:8080",
        "describo": "http://localhost:8090"
    }
},
```

If you use the owncloud classic backend, you will need to install the php dependencies, too.

```bash
composer install --working-dir=client/packages/classic/php
```

### Server setup

Install the python dependencies.

```bash
cd server
pipenv install
```

### Start the development environments

For easier access, we provide a makefile in root folder.

**Beware: For development and production, you need access to a working RDS instance. For example through VPN with `openconnect` or a ssh tunnel `ssh -L 1443:<your-k8s-rds-installation>:443 <jumphost>.<institution>` to an already existing one or use minikube for smaller test environments. [See this guide for more](https://www.research-data-services.org/doc/getting-started/k8s/).**

If you want to start the environment for standalone, use the `standalone` receipt.

```bash
make standalone
```

If you want to start the environment for owncloud classic with classic ui, use the `classic` receipt.

```bash
make classic
```

If you want to start the environment for ownclouds new ui OC Web with classic backend, use the `web` receipt.

```bash
make web
```

If you want to start the environment for owncloud new ui OC Web with ocis backend, we currently have no receipt.

### Run tests

Runs the tests for vue and python after each other. If the first one fails, then the second one will not executed.

```
make test
```

### Compiles and minifies for production in standalone

We use docker to create containers. This will build a single server, which serves the frontend under port 8080.
This can be build with the following command, which will be stored in the local container storage under the name "rds-web".

```
docker build -t rds-web
```

### Lints and fixes files

```
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

## Client Localization

We are using `vue-gettext-cli` for the localization of our client app. You can find a tutorial on their [github page](https://github.com/Polyconseil/vue-gettext#use-the-component-or-the-directive). With the following command, every localizaton will be find in the client source code.

```bash
make l10n-extract
```

After the extraction, you can change the placeholders in folder `/client/packages/codebase/translations/locales` in any needed language (currently configured: englisch (default), german). Now, you need to compile it for loading with the following command:

```bash
make l10n-compile
```

Now, you have to build and distribute your client app again. In our case, it will be published through a docker container.

# Token Storage <-> Describo decoupling

Because of the mechanic behind describo, there is a need for a helper functionality. Describo needs some informations to setup a session. This session and the corresponding id will be presented to the user via websocket through the python server. At this point, describo already needs the access token from sciebo RDS, but this token will be refreshed every 60 minutes automatically, so the first access token will be invalid at this time. So there comes the helper functionality into play, which listens for such an event to update the corresponding session id, so the user does not take any notice of this procedure. The helper functionality is implemented in rust in the `helper` microservice`. The token storage publishes the event via the already used redis within a pubsub-key. The helper will take notice of this and lookup for the corresponding username and the session id for describo in redis (which will be placed by the python server for later usage for example in replicas). So the helper will make the request to update the new access token in describo without the need to create a separate thread in the python server. The rust helper microservice is so limited and easy, you can understand it without deep knowledge of rust. :) It is already build with replicants and many requests in pipeline in mind.

# Docker Deployment

We use an internal gitlab to build and store the docker container. But it is public available, so please take a look at our [gitlab registry](https://zivgitlab.uni-muenster.de/sciebo-rds/RDS-Web/-/packages) to get the container. The pipeline will be triggered for all branches, so you can easily create a pull request and take advantage of this "easy to use"-pipeline.

You can use the RDS-Web docker container with this url: `zivgitlab.wwu.io/sciebo-rds/RDS-Web:<TAG>`. The following table show you all needed tags.

| Tag            | Description                                                                                                                          |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| latest         | The latest build over all branches. This is not recommended for production use.                                                      |
| main           | The latest build for the `main` branch. Not for production use.                                                                      |
| `<NUMBER>`     | The build with pipeline-identifier `<NUMBER>`. For production use, set your wanted identifier, so you get always the same container. |
| `<BRANCHNAME>` | The same like `main`, but for general branchnames.                                                                                   |

Setting up the RDS instance
---------------------------

Here we will deploy a local instance of RDS on a minikube environment.
Many of the instructions here are copied from the instructions at `../setup-local-dev-env.md`,
adapted to an embedded deployment rather than a standalone one,
so it will be worth to check that document as well.

I have tested all this both in Debian 10.13 and in ubuntu 22.04 and in archlinux 2023-03-01 VMs .

Prerequisites:

 * kubectl (tested with version 1.26.1 (server) and 1.25.3 (client))
 * Minikube (tested with version 1.29.0)
 * Docker (tested with versions 23.0.0 and 23.0.1)
 * helm (tested with version 3.11.0)

We also want to register an app with Zenodo's sandbox and/or OFS test site.
To configure the app at those repositories,
we use `https://test-rds.localdomain.test`
as both Website URL and Redirect URI
(unless we change these values in the provided `values.yaml` file).

First we check out the code for the charts.

    $ git clone git@github.com:Sciebo-RDS/charts

NOTE: as of now (08-03-2023) we need to check out a patched version of the charts,
https://github.com/enriquepablo/charts/tree/minikube-nextcloud

Then we prepare our [values.yaml](values.yaml) configuration file for the k8s environment.
The provided file should only need edition to add the OAuth2 client IDs and secrets,
as we will see below.

Some values in that file that we may want to adapt:

`global.image.tag`
:This has to correspond with the RDS version we want to deploy

`global.describo.domain`, `global.rds.domain`
:Domain names where describo and rds will be served. The default `test-rds.localdomain.test` and `` should be fine for most cases. We will later point them to the minikube IP in `/etc/hosts`.

`global.domains`
:Domain names where OwnCloud or NextCloud instances will be served. We start with no entries here; later, when we add the RDS instance as OAuth2 client for nextcloud, we will add one entry; we might have more than one entries here. Each entry will need a `name` that coincides with the domain name in the cloudIds provided by that EFSS, an address where it can be found, and OAuth2 client ID and secret for the RDS instance, we will create these later when we deploy and configure the EFSS.

`layer1-port-zenodo.environment`
:To publish to Zenodo, we need to register our RDS instance as an OAuth2 client for zenodo, and set here the clinet ID and secret.

`layer1-port-openscienceframework.environment`
:To publish to OFS, we need to register our RDS instance as an OAuth2 client for OFS, and set here the client ID and secret.

If you decide to not configure either zenodo of OFS, remember to set its `enabled` flag to false.

We can leave the rest of the values as provided.

Now we deploy the k8s environment with minikube. First we start from a clean slate:

    $ minukube stop && minikube delete

Then we set docker as the minikube driver, and start the minikube env:

    $ minikube config set driver docker
    $ minikube start --kubernetes-version=v1.26.0 --memory=5g

Then we enable ingress and create the namespace we have set in `values.yaml`, in `global.namespace.name`:

    $ minikube addons enable ingress
    $ kubectl create ns rds

At this point we can check the minikube IP and add the `global.describo.domain` and `global.rds.domain` to `/etc/hosts`, pointing at that IP:

    $ minikube ip
    192.168.49.2

If we want to deploy some local changes, via providing a local docker image for some k8s service,
now is the time to build the image.
If, for example, we are editing the RDS javascript code, we will want to provide locally the image for the layer0-web pods.
To build the image we need to edit the dockerfile and remove the `zivgitlab.uni-muenster.de/sciebo-rds/dependency_proxy/containers/`
prefixes from the FROM directives - so, for example, we would have `FROM node:16-alpine3.16 AS staging`.

    $ cd RDS/layer0_ingress/web/
    $ vim Dockerfile.rds-standlalone
    $ eval $(minikube -p minikube docker-env)  # this points the current terminal to the minikube docker environment
    $ docker build -f Dockerfile.rds-standalone -t rds-app:0.10 .
    $ docker tag rds-app:0.10 zivgitlab.wwu.io/rds-app:v0.2.2

And now we can configure our values.yaml file to use the built image:

    layer0-web:
      image:
        repository: rds-app
        pullPolicy: Never

Now we use the [provided script](build-all-dependencies-with-helm.sh) to build and update the helm charts:

    $ bash build-all-dependencies-with-helm.sh

And finally we  deploy the RDS stuff to the newly created environment:

    $ helm upgrade -n rds sciebords ./charts/charts/all/ -i --values values.yaml

After a while, the following pods should be up and running:

    $ kubectl get po -A
    NAMESPACE       NAME                                                    READY   STATUS             RESTARTS        AGE
    ingress-nginx   ingress-nginx-admission-create-f299n                    0/1     Completed          0               31m
    ingress-nginx   ingress-nginx-admission-patch-bd258                     0/1     Completed          0               31m
    ingress-nginx   ingress-nginx-controller-87c64747b-29zhr                1/1     Running            0               31m
    kube-system     coredns-565d847f94-rq2tz                                1/1     Running            0               31m
    kube-system     etcd-minikube                                           1/1     Running            0               31m
    kube-system     kube-apiserver-minikube                                 1/1     Running            0               31m
    kube-system     kube-controller-manager-minikube                        1/1     Running            0               31m
    kube-system     kube-proxy-l8k9n                                        1/1     Running            0               31m
    kube-system     kube-scheduler-minikube                                 1/1     Running            0               31m
    kube-system     storage-provisioner                                     1/1     Running            1 (30m ago)     31m
    rds             layer0-describo-65859fb5bb-2nmxh                        2/2     Running            0               14m
    rds             layer0-helper-describo-token-updater-5d4978747c-64bhk   1/1     Running            1 (7m19s ago)   14m
    rds             layer0-web-9944cf776-cpg99                              0/1     CrashLoopBackOff   6 (12s ago)     14m
    rds             layer1-port-owncloud-test-adress-de-85cd85d988-rvz5p    0/1     CrashLoopBackOff   6 (8s ago)      14m
    rds             layer1-port-zenodo-57bb76944b-6lhn6                     1/1     Running            2 (6m21s ago)   14m
    rds             layer2-exporter-service-67ddcffc94-vgdj5                1/1     Running            0               14m
    rds             layer2-metadata-service-74cddf5478-mwp48                1/1     Running            0               14m
    rds             layer2-port-service-664c4c5fff-g88zz                    1/1     Running            0               14m
    rds             layer3-research-manager-7bd4677dc-lbrnv                 1/1     Running            0               14m
    rds             layer3-token-storage-5d45bdf469-kw2xj                   1/1     Running            0               14m
    rds             nextcloud-5b5b757489-6bj8h                              1/1     Running            0               14m
    rds             postgresql-0                                            1/1     Running            0               14m
    rds             redis-0                                                 1/1     Running            1 (6m6s ago)    14m
    rds             redis-1                                                 1/1     Running            1 (6m9s ago)    14m
    rds             redis-2                                                 1/1     Running            0               14m
    rds             redis-3                                                 1/1     Running            0               14m
    rds             redis-4                                                 1/1     Running            0               14m
    rds             redis-5                                                 1/1     Running            1 (6m7s ago)    14m
    rds             redis-helper-master-0                                   1/1     Running            0               14m

The problems with layer0-web and layer1-port-owncloud-test-address-de will get fixed once we set RDS as nextcloud OAuth2 client next.
Note that the last part of the pod names will vary from deployment to deployment.


Setting up NextCloud
--------------------

We will host the NextCloud instance under `test-nextcloud.localdomain.test`,
so first, in `/etc/hosts`, we point that name to minikube's IP.

Now we will install the RDS app into nextcloud.
First we get the softare, and build it:

    $ git clone https://github.com/Sciebo-RDS/plugin-nextcloud
    $ cp -R plugin-nextcloud/nextcloud-rds rds
    $ cd rds
    $ make
    $ cd ..
    $ kubectl cp -n rds rds <name of nextcloud pod>:/var/www/html/apps

If the `make` command complains about versions, just remove the `composer.lock` file.

Now you should be able to enable the RDS app in the web interface of NextCloud
with an admin account (by default, admin:password), go to apps and look for it and enable it.

Now we want to add RDS as an OAuth2 client in NextCloud.
Go to administration settings -> security and add a client,
named `rds` and with redirection URI `https://test-rds.localdomain.test`
(unless you chaged this value in `values.yaml`).

Add the created OAuth2 client ID and secret to values.yaml, at `global.domains`,
adding an entry like this:

    domains:
      - name: test-nextcloud.localdomain.test # name needs to be exact the same as the second part after last @ in the cloudId
        INTERNAL_ADDRESS: http://nextcloud:8080
        ADDRESS: https://test-nextcloud.localdomain.test
        OAUTH_CLIENT_ID: QoS7peuwYEF7NKMY5xhc4NLOOVLQIZwgKltav4dBdfuOHplQvmKuuCZUs2RJoEdy
        OAUTH_CLIENT_SECRET: 79OcQEz3M7I5bJU8jCDvxu9CtNk2O7qY12rlByAmqGiXdYy04OMAnJ1AFOGTcNCq
        SUPPORT_EMAIL: mail@localdomain.test
        MANUAL_URL: usermanual.localdomain.test

And update the helm release:

    $ helm upgrade -n rds sciebords ./charts/charts/all/ -i --values values.yaml

Then, configure the RDS app, in administration settings -> additional settings.
Set `https://test-rds.localdomain.test` as the URL, and `rds` as the name.
The name `rds` can be any other name, as long as it's the same as the one provided
for the OAuth2 client.

Then, create the keys for the RDS app:

    $ minikube ssh
    $ docker ps |grep k8s_nextcloud |awk '{print $1}'
    <container id>
    $ docker exec -u www-data <container id> bash -c "/var/www/html/occ rds:create-keys"


Setting up OwnCloud
--------------------

We will host the OwnCloud instance under `test-owncloud.localdomain.test`,
so first, in `/etc/hosts`, we point that name to minikube's IP.

In OwnCloud, OAuth2 is provided by an app,
so first thing is to enable the OAuth2 app,
via admin settings -> apps,
since the app comes preloaded with OwnCloud.

Now we will install the RDS app into owncloud.
It is in the owncloud market, so to install it,
we use the market app (accessible in the top left meny in OwnCloud).
Click on the "integrations" category and look for "Research Data Services",
click on it, and install it.

Now we want to add RDS as an OAuth2 client in OwnCloud.
Go to "administration settings -> user authentication" and add a client,
named `rds` and with redirection URI `https://test-rds.localdomain.test`
(unless you chaged this value in `values.yaml`).

Add the created OAuth2 client ID and secret to values.yaml, at `global.domains`,
adding an entry like this:

    domains:
      - name: test-owncloud.localdomain.test # name needs to be exact the same as the second part after last @ in the cloudId
        INTERNAL_ADDRESS: http://owncloud:8080
        ADDRESS: https://test-owncloud.localdomain.test
        OAUTH_CLIENT_ID: QoS7peuwYEF7NKMY5xhc4NLOOVLQIZwgKltav4dBdfuOHplQvmKuuCZUs2RJoEdy
        OAUTH_CLIENT_SECRET: 79OcQEz3M7I5bJU8jCDvxu9CtNk2O7qY12rlByAmqGiXdYy04OMAnJ1AFOGTcNCq
        SUPPORT_EMAIL: mail@localdomain.test
        MANUAL_URL: usermanual.localdomain.test

And update the helm release:

    $ helm upgrade -n rds sciebords ./charts/charts/all/ -i --values values.yaml

Then, configure the RDS app, in administration settings -> research data services.
Set `https://test-rds.localdomain.test` as the URL, and `rds` as the name.
The name `rds` can be any other name, as long as it's the same as the one provided
for the OAuth2 client.

Then, create the keys for the RDS app:

    $ minikube ssh
    $ docker ps |grep k8s_owncloud |awk '{print $1}'
    <container id>
    $ docker exec -u www-data <container id> bash -c "/var/www/owncloud/occ rds:create-keys"


Patching sources
----------------

For RDS versions 0.2.3 and below, we need to add a couple of patches to the sources,
at 2 different pods. In essence, without the EFSS (nextcloud in this case)
being available at a public IP, we need 2 addresses to access it,
one from the other pods and one from the browser. Hopefully this will be
fixed in future versions, but I'll provide instructions here nevertheless,
to demonstate how to patch the system for development and debugging.

Note that this method is fairly brittle; as soon as k8s restarts some pod's container,
the patches will be lost. To make the changes more permanent,
they should be added to the images that k8s has available to run its containers.
This method is suited for Python patches, that do not need compilation or transpilation,
and is more agile than putting the changes in a new docker image.

So at this point, we want to patch the layer0-web service with the Python changes
[in this PR](https://github.com/Sciebo-RDS/Sciebo-RDS/pull/241/files).

In essence, we access the pods using docker, from the minikube container.
For example:

    $ minikube ssh
    $ docker ps |grep k8s_layer0-web |awk '{print $1}'
    <container id>
    $ docker cp <container id>:/srv/src/app.py .
    $ vi app.py
    $ docker cp app.py <container id>:/srv/src/app.py
    $ docker restart <container id>

NOTE XXX: The patch for the layer1-port-owncloud services
provided in the linked PR will not work: the service entry in the db
was created when the k8s service was created,
and so, it will contain a wrong refresh_url.
So we now patch /app/lib/TokenService.py in layer2-port-service
and hardcode the refresh_url there, to `http://nextcloud:8080`.
This would be the patch:

    diff --git a/RDS/layer2_use_cases/port/src/lib/TokenService.py b/RDS/layer2_use_cases/port/src/lib/TokenService.py
    index 6489e23..f17cb4a 100644
    --- a/RDS/layer2_use_cases/port/src/lib/TokenService.py
    +++ b/RDS/layer2_use_cases/port/src/lib/TokenService.py
    @@ -525,8 +525,15 @@ class TokenService:

             logger.info(f"request body: {body}")

    +        refresh_url_new = f"{service.refresh_url}"
    +        if 'test-nextcloud' in refresh_url_new:
    +            refresh_url_new = "http://nextcloud:8080/index.php/apps/oauth2/api/v1/token"
    +        elif 'test-owncloud' in refresh_url_new:
    +            refresh_url_new = "http://owncloud:8080/index.php/apps/oauth2/api/v1/token"
    +
             response = requests.post(
    -            f"{service.refresh_url}",
    +            # XXX only needed until the INTERNAL_ADDRESS patch is accepted
    +            refresh_url_new,
                 data=body,
                 auth=(service.client_id, service.client_secret),
                 verify=(os.environ.get("VERIFY_SSL", "True") == "True"),

And finally, you should be able to use RDS from within the NextCloud / OwnCloud instance.
Remember to add an email address to your NextCloud / OwnCloud account,
or you won't be authorized to access RDS.


Debugging
---------

The above patching method will be effective to patch Python sources.
If instead, we want to patch js, or go, or rust code, we will have to do a bit more work:
we will have to use the patched code to build docker images and use those new images
in the k8s environment. [Dave's instructions](../setup-local-dev-env.md) provide some directions to do so.

What follows is an example of editing the js RDS code,
transpiling it via building the docker image that would hold the bundle,
extracting the transpiled js bundle from the image,
and injecting it into the corresponding container in the minikube environment.

So, we start by editing the js code at `Sciebo-RDS/RDS/layer0_ingress/web/client/packages/codebase`.

Then we build the docker image.
The appropriate dockerfile is `Sciebo-RDS/RDS/layer0_ingress/web/Dockerfile.rds-standalone`.
Unless you are within the Münster University network,
you'll need to edit the dockerfile and remove references to it.
I also found that I needed to add some `ARG` and `ENV` directives to the dockerfile
to get a functional js bundle.
These are the changes that worked for me to produce a working js bundle:

    $ git diff Dockerfile.rds-standalone
    diff --git a/RDS/layer0_ingress/web/Dockerfile.rds-standalone b/RDS/layer0_ingress/web/Dockerfile.rds-standalone
    index 85add8d0..6294e89d 100644
    --- a/RDS/layer0_ingress/web/Dockerfile.rds-standalone
    +++ b/RDS/layer0_ingress/web/Dockerfile.rds-standalone
    @@ -1,13 +1,20 @@
    -FROM zivgitlab.uni-muenster.de/sciebo-rds/dependency_proxy/containers/node:16-alpine3.16 AS staging
    +FROM node:16-alpine3.16 AS staging
     WORKDIR /src
     RUN apk add findutils
     COPY client .
     RUN mkdir -p ./pkg/ \
         && find . -type d -name node_modules -prune -false -o \( -name "package.json" -o -name "yarn.lock" -o -name "package-lock.json" \)  -exec install -D '{}' './pkg/{}' \;

    -FROM zivgitlab.uni-muenster.de/sciebo-rds/dependency_proxy/containers/node:16-alpine3.16 AS web
    +FROM node:16-alpine3.16 AS web
     WORKDIR /app
    +ARG VUE_APP_BASE_URL
    +ARG VUE_APP_FRONTENDHOST
    +ARG SOCKETIO_HOST
    +ARG SOCKETIO_PATH
     ENV VUE_APP_BASE_URL $VUE_APP_BASE_URL
    +ENV VUE_APP_FRONTENDHOST $VUE_APP_FRONTENDHOST
    +ENV SOCKETIO_HOST $SOCKETIO_HOST
    +ENV SOCKETIO_PATH $SOCKETIO_PATH
     WORKDIR /app
     RUN apk add --no-cache gettext python3 build-base make && python3 -m ensurepip && pip3 install --no-cache --upgrade pip setuptools
     COPY --from=staging /src/pkg ./
    @@ -15,14 +22,22 @@ RUN yarn install --non-interactive
     COPY client .
     RUN yarn standalone

    -FROM zivgitlab.uni-muenster.de/sciebo-rds/dependency_proxy/containers/python:3.8-alpine
    +FROM python:3.8-alpine
     WORKDIR /srv

     EXPOSE 80

    +ARG VUE_APP_BASE_URL
    +ARG VUE_APP_FRONTENDHOST
    +ARG SOCKETIO_HOST
    +ARG SOCKETIO_PATH
    +ENV VUE_APP_BASE_URL $VUE_APP_BASE_URL
    +ENV VUE_APP_FRONTENDHOST $VUE_APP_FRONTENDHOST
    +ENV SOCKETIO_HOST $SOCKETIO_HOST
    +ENV SOCKETIO_PATH $SOCKETIO_PATH
    +
     ENV JSFOLDER=/usr/share/nginx/html/js/*.js

    -ENV SOCKETIO_HOST=http://localhost:80
     ENV REDIS_HELPER_HOST=http://owncloud_redis
     ENV REDIS_HELPER_PORT=6379
     ENV PROMETHEUS_MULTIPROC_DIR=/tmp


Then build the image, start a container from it, get the built js bundle, and get rid of image and container:

    $ docker build -f Dockerfile.rds-standalone -t rds-app:0.10 --build-arg VUE_APP_BASE_URL="/" --build-arg VUE_APP_FRONTENDHOST="https://test-rds.localdomain.test" --build-arg SOCKETIO_HOST="https://test-rds.localdomain.test" --build-arg SOCKETIO_PATH="/socket.io/" .
    $ docker run -d --rm --entrypoint="sleep" rds-app:0.10 infinity
    <container id 1>
    $ docker cp <container id 1>:/usr/share/nginx/html/js/app.js app-rds.js
    $ docker stop <container id 1>
    $ docker rmi rds-app:0.10
    $ docker ps |grep minikube | awk '{print $1}'
    <container id 2>
    $ docker cp app-rds.js <container id 2>:/home/docker
    $ minikube ssh
    $ docker ps |grep k8s_layer0-web | awk '{print $1}'
    <container id 3>
    $ docker cp app-rds.js <container id 3>:/usr/share/nginx/html/js/app.js
    $ rm /app-rds.js
    $ exit
    $ rm app-rds.js


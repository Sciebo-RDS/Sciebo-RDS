
Setting up the RDS instance
---------------------------

Here we will deploy a local instance of RDS on a minikube environment.

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
    $ minikube start --kubernetes-version=v1.25.3 --memory=5g

Then we enable ingress and create the namespace we have set in `values.yaml`, in `global.namespace.name`:

    $ minikube addons enable ingress
    $ kubectl create ns rds

At this point we can check the minikube IP and add the `global.describo.domain` and `global.rds.domain` to `/etc/hosts`, pointing at that IP:

    $ minikube ip
    192.168.49.2

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


Patching sources
----------------

For RDS version 0.2.2, we need to add a couple of patches to the sources,
at 2 different pods. In essence, without the EFSS (nextcloud in this case)
being available at a public IP, we need 2 addresses to access it,
one from the other pods and one from the browser. Hopefully this will be
fixed in future versions, but I'll provide instructions here nevertheless,
to demonstate how to patch the system for development and debugging.
There may be a better method, but this works for me.

So at this point, we want to patch the layer0-web service with this code:

    diff --git a/RDS/layer0_ingress/web/server/src/Describo.py b/RDS/layer0_ingress/web/server/src/Describo.py
    index 3fcddd2..01242fe 100644
    --- a/RDS/layer0_ingress/web/server/src/Describo.py
    +++ b/RDS/layer0_ingress/web/server/src/Describo.py
    @@ -1,7 +1,7 @@
     import os
     import requests
     from flask import session
    -from .app import app
    +from .app import app, domains_dict


     def getSessionId(access_token=None, folder=None):
    @@ -12,13 +12,19 @@ def getSessionId(access_token=None, folder=None):

         _, _, servername = informations["cloudID"].rpartition("@")

    +    webdav_url = None
         if servername is not None:
    -        servername = "https://{}/remote.php/dav".format(servername)
    +        server_info = domains_dict.get(servername.replace('.', '-'))
    +        if server_info is not None and 'INTERNAL_ADDRESS' in server_info:
    +            webdav_url = server_info['INTERNAL_ADDRESS'] + '/remote.php/dav'
    +
    +        if webdav_url is None:
    +            webdav_url = "https://{}/remote.php/dav".format(servername)

         data = {
             # needs to be UID, because webdav checks against UID
             "user_id": informations["UID"],
    -        "url": servername or default,
    +        "url": webdav_url or default,
         }

         if access_token is not None:
    diff --git a/RDS/layer0_ingress/web/server/src/app.py b/RDS/layer0_ingress/web/server/src/app.py
    index e1960b1..847ae3a 100644
    --- a/RDS/layer0_ingress/web/server/src/app.py
    +++ b/RDS/layer0_ingress/web/server/src/app.py
    @@ -74,7 +74,7 @@ class DomainsDict(UserDict):
             except KeyError:
                 status_code = 500
                 req = None
    -            url = self[key]["ADDRESS"]
    +            url = self[key].get("INTERNAL_ADDRESS", self[key]["ADDRESS"])
                 count = 5

                 while status_code > 200 and count > 0:
    diff --git a/RDS/layer0_ingress/web/server/src/server.py b/RDS/layer0_ingress/web/server/src/server.py
    index 52eb5ee..caa1c9d 100644
    --- a/RDS/layer0_ingress/web/server/src/server.py
    +++ b/RDS/layer0_ingress/web/server/src/server.py
    @@ -88,7 +88,7 @@ class User(UserMixin):
                 headers = {"Authorization": f"Bearer {token}"}

                 for key, domain in domains_dict.items():
    -                url = domain["ADDRESS"] or os.getenv(
    +                url = domain.get("INTERNAL_ADDRESS", domain["ADDRESS"]) or os.getenv(
                         "OWNCLOUD_URL", "https://localhost/index.php"
                     )

Also we wnat to patch the layer1-port-owncloud service with this:

    diff --git a/RDS/layer1_adapters_and_ports/port_owncloud/src/server.py b/RDS/layer1_adapters_and_ports/port_owncloud/src/server.py
    index ad60210..e8b4802 100644
    --- a/RDS/layer1_adapters_and_ports/port_owncloud/src/server.py
    +++ b/RDS/layer1_adapters_and_ports/port_owncloud/src/server.py
    @@ -6,9 +6,10 @@ from RDS import Util
     import os

     owncloud_installation_url = os.getenv("OWNCLOUD_INSTALLATION_URL", "")
    +owncloud_internal_installation_url = os.getenv("OWNCLOUD_INTERNAL_INSTALLATION_URL", "")
     owncloud_redirect_uri = os.getenv("RDS_OAUTH_REDIRECT_URI", "")
     owncloud_oauth_token_url = "{}/index.php/apps/oauth2/api/v1/token".format(
    -    owncloud_installation_url
    +    owncloud_internal_installation_url
     )
     owncloud_oauth_id = os.getenv("OWNCLOUD_OAUTH_CLIENT_ID", "XY")
     owncloud_oauth_secret = os.getenv("OWNCLOUD_OAUTH_CLIENT_SECRET", "ABC")

In essence, we access the pods using docker, from the minikube container.

    $ minikube ssh
    $ docker ps |grep k8s_layer0-web |awk '{print $1}'
    <container id>
    $ docker cp <container id>:/srv/src/app.py .
    $ vi app.py
    $ docker cp app.py <container id>:/srv/src/app.py
    $ docker cp <container id>:/srv/src/server.py .
    $ vi server.py
    $ docker cp server.py <container id>:/srv/src/server.py
    $ docker cp <container id>:/srv/src/Describo.py .
    $ vi Describo.py
    $ docker cp Describo.py <container id>:/srv/src/Describo.py
    $ docker restart <container id>

Repeat same process for the layer1-port-owncloud-test-nextcloud-localdomain-test service.

    $ minikube ssh
    $ docker ps |grep k8s_layer1-port-owncloud |awk '{print $1}'
    <container id>
    $ docker cp <container id>:/app/server.py .
    $ vi server.py
    $ docker cp server.py <container id>:/app/server.py
    $ docker restart <container id>

NOTE XXX: This last patch will not work: the service entry in the db
was created when the k8s service was created,
and so, it will contain a wrong refresh_url.
So we now patch /app/lib/TokenService.py in layer2-port-service
and hardcode the refresh_url there, to `http://nextcloud:8080`.
This would be the patch:

    diff --git a/RDS/layer2_use_cases/port/src/lib/TokenService.py b/RDS/layer2_use_cases/port/src/lib/TokenService.py
    index 6489e23..f17cb4a 100644
    --- a/RDS/layer2_use_cases/port/src/lib/TokenService.py
    +++ b/RDS/layer2_use_cases/port/src/lib/TokenService.py
    @@ -525,8 +525,13 @@ class TokenService:

             logger.info(f"request body: {body}")

    +        refresh_url_new = f"{service.refresh_url}"
    +        if 'nextcloud' in refresh_url_new:
    +            refresh_url_new = "http://nextcloud:8080/index.php/apps/oauth2/api/v1/token"
    +
             response = requests.post(
    -            f"{service.refresh_url}",
    +            # XXX only needed until the INTERNAL_ADDRESS patch is accepted
    +            refresh_url_new,
                 data=body,
                 auth=(service.client_id, service.client_secret),
                 verify=(os.environ.get("VERIFY_SSL", "True") == "True"),

And finally, you should be able to use RDS from within the NextCloud instance.
Remember to add an email address to your NextCloud account,
or you won't be authorized to access RDS.

The above patching method will be effective to patch Python sources.
If instead, we want to patch js, or go, or rust code, we will have to do a bit more work:
we will have to use the patched code to build docker images and use those new images
in the k8s environment. [Dave's instructions](../setup-local-dev-env.md) provide some directions to do so.

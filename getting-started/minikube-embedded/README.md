
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
 * helm (tested with version 3.11.0 and 3.11.2)

We also want to register an app with Zenodo's sandbox and/or OFS test site.
To configure the app at those repositories,
we use `https://test-rds.localdomain.test`
as both Website URL and Redirect URI
(unless we change these values in the provided `values.yaml` file).

First we check out the code for the charts.

    $ git clone git@github.com:Sciebo-RDS/charts

If we are going to patch sources and rebuild docker images to test the changes,
we also need the RDS code:

    $ git clone git@github.com:Sciebo-RDS/Sciebo-RDS

Then we prepare our [values.yaml](values.yaml) configuration file for the k8s environment.
The provided file should only need edition to add the `global.domains` for OwnCLoud and NextCloud,
and the OAuth2 client IDs and secrets for zenodo and/or OFS,
as we will see below.

Some values in that file that we may want to adapt:

`global.image.tag`
:This has to correspond with the RDS version we want to deploy

`global.describo.domain`, `global.rds.domain`
:Domain names where describo and rds will be served. The default `test-rds.localdomain.test` and `` should be fine for most cases. We will later point them to the minikube IP in `/etc/hosts`.

`global.domains`
:Domain names where OwnCloud or NextCloud instances will be served. We start with no entries here; later, when we add the RDS instance as OAuth2 client for nextcloud, we will add one entry; we might have more than one entries here. Each entry will need a `name` that coincides with the domain name in the cloudIds provided by that EFSS, an address where it can be found, and OAuth2 client ID and secret for the RDS instance, we will create these later when we deploy and configure the EFSS.

`layer1-port-zenodo.environment`
:To publish to Zenodo, we need to register our RDS instance as an OAuth2 client for zenodo, and set here the client ID and secret.

`layer1-port-openscienceframework.environment`
:To publish to OFS, we need to register our RDS instance as an OAuth2 client for OFS, and set here the client ID and secret.

If you decide to not configure either zenodo of OFS, remember to set its `enabled` flag to false, and to comment out the corresponding section.

We can leave the rest of the values as provided.

Now we deploy the k8s environment with minikube. First we start from a clean slate:

    $ minukube stop && minikube delete

Then we set docker as the minikube driver, and start the minikube env:

    $ minikube config set driver docker
    $ minikube start --kubernetes-version=v1.26.1 --memory=5g

Then we enable ingress and create the namespace we have set in `values.yaml`, in `global.namespace.name`:

    $ minikube addons enable ingress
    $ kubectl create ns rds

At this point we can check the minikube IP and add the `global.describo.domain` and `global.rds.domain` to `/etc/hosts`, pointing at that IP:

    $ minikube ip
    192.168.49.2

If we want to deploy some local changes, via providing a local docker image for some k8s service,
now is the time to build the image. We will do this in the Sciebo-RDS cloned repository.

If, for example, we are editing the RDS javascript code, we will want to provide locally the image for the layer0-web pods.
To build the image we need to edit the dockerfile and remove the `zivgitlab.uni-muenster.de/sciebo-rds/dependency_proxy/containers/`
prefixes from the FROM directives - so, for example, we would have `FROM node:16-alpine3.16 AS staging` instead of
`FROM zivgitlab.uni-muenster.de/sciebo-rds/dependency_proxy/containers/node:16-alpine3.16 AS staging`.

    $ cd RDS/layer0_ingress/web/
    $ vim Dockerfile.rds-standalone
    $ eval $(minikube -p minikube docker-env)  # this points the current terminal to the minikube docker environment
    $ docker build -f Dockerfile.rds-standalone -t rds-app:0.10 .
    $ docker tag rds-app:0.10 zivgitlab.wwu.io/rds-app:v0.2.3

And now we can configure our values.yaml file to use the built image:

    layer0-web:
      image:
        repository: rds-app
        pullPolicy: Never

Note that as of version 0.2.3, and until these
to work on minikube we need to build the images locally for both layer0-web
(as shown above) and layer1-port-owncloud (as shown below).

To build the layer1-port-owncloud docker image:

    $ cd RDS/layer1_adapters_and_ports/port_owncloud
    $ vim dockerfile  # Remove the `zivgitlab.uni-muenster.de/sciebo-rds/dependency_proxy/containers/` prefix from the FROM directive
    $ eval $(minikube -p minikube docker-env)  # this points the current terminal to the minikube docker environment
    $ docker build -f dockerfile -t rds-port-owncloud:0.10 .
    $ docker tag rds-port-owncloud:0.10 zivgitlab.wwu.io/rds-port-owncloud:v0.2.3

And add to values.yaml:

    layer1-port-owncloud:
      image:
        repository: rds-port-owncloud
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

The problems with layer0-web and layer1-port-owncloud-test-address-de will get fixed once we set RDS as nextcloud & owncloud OAuth2 client next.
Note that the last part of the pod names will vary from deployment to deployment.


Setting up NextCloud
--------------------

We will host the NextCloud instance under `test-nextcloud.localdomain.test`,
so first, in `/etc/hosts`, we point that name to minikube's IP.

Now we will install the RDS app into nextcloud.
First we get the software, and build it:

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
        OAUTH_CLIENT_ID: QoS7...oEdy
        OAUTH_CLIENT_SECRET: 79O...NCq
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

And finally, you should be able to use RDS from within the NextCloud instance.
Remember to add an email address to your NextCloud account,
or you won't be authorized to access RDS.


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
        OAUTH_CLIENT_ID: QoS7...oEdy
        OAUTH_CLIENT_SECRET: 79Oc...NCq
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

And finally, you should be able to use RDS from within the OwnCloud instance.
Remember to add an email address to your OwnCloud account,
or you won't be authorized to access RDS.


Patching sources
----------------

Here I provide a method to rapidly test changes to python code,
simply using `docker cp` to push Python modules into containers.

Note that this method is fairly brittle; as soon as k8s restarts some pod's container,
the patches will be lost. To make the changes more permanent,
they should be added to the images that k8s has available to run its containers.
This method is only suited for Python patches, that do not need compilation or transpilation;
for js or rust of go patches, we'd need to rebuild the docker images.

So at this point, we want for example to patch the layer0-web service
with changes to the `app.py` module. 

In essence, we access the pods using docker, from the minikube container.
For example:

    $ minikube ssh
    $ docker ps |grep k8s_layer0-web |awk '{print $1}'
    <container id>
    $ docker cp <container id>:/srv/src/app.py .
    $ vi app.py
    $ docker cp app.py <container id>:/srv/src/app.py
    $ docker restart <container id>

After this, the layer0-web service should run with the modified code.

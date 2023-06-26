# Developing for RDS with minikube

The aim of this documentation is to show how to deploy an RDS instance in a
minikube environment, and how to use it for development.

## Basic setup

We will be working on a dedicated directory, e.g. `~/RDS/`. All the commands
will be assumed to be executed there (unless stated otherwise) and all needed
files will be assumed to be placed there.

## Setting up the bare minikube environment

This has been tested in Debian 10.13, ubuntu 22.04, and archlinux 2023-03-01
VMs.

Prerequisites of software:

 * kubectl (tested with version 1.26.1 (server) and 1.25.3 (client))
 * Minikube (tested with version 1.29.0)
 * Docker (tested with versions 23.0.0 and 23.0.1)
 * helm (tested with version 3.11.0 and 3.11.2)

We need the Docker daemon running.

First we start from a clean slate:

    $ minukube stop && minikube delete

Then we set docker as the minikube driver, and start the minikube env:

    $ minikube config set driver docker
    $ minikube start --kubernetes-version=v1.26.1 --memory=5g

Then we enable ingress and create a namespace named `rds`. If you want to
change the name, you have to reflect the changes in the `values.yaml` for helm,
described below.

    $ minikube addons enable ingress
    $ kubectl create ns rds

## Setting up the RDS instance

First we check out the code for the Helm charts.

    $ git clone git@github.com:Sciebo-RDS/charts

We check out the RDS code. We need this to get the appropriate initial `values.yaml` file
and the script to build the Helm dependencies (see below). This code is also needed
if we are going to patch sources and rebuild docker images to test the changes.

    $ git clone git@github.com:Sciebo-RDS/Sciebo-RDS

Then we prepare our `values.yaml` configuration file to build the k8s environment with Helm.
The provided file (in the Sciebo-RDS repo at path `/getting-started/minikube-embedded/values.yaml`)
should only need edition to add the `global.domains` for OwnCLoud and NextCloud,
and the OAuth2 client IDs and secrets for Zenodo and/or OSF,
as we will see below.

    $ cp Sciebo-RDS/getting-started/minikube-embedded/values.yaml .

Some values in that file that we may want to adapt:

`global.image.tag`
: This has to correspond with the RDS version we want to deploy. Should be 0.2.4 or above.

`global.describo.domain`, `global.rds.domain`
: Domain names where describo and rds will be served. The default `test-describo.localdomain.test` and `test-rds.localdomain.test` should be fine for most cases. We will later point them to the minikube IP in `/etc/hosts`.

`global.domains`
: Domains where OwnCloud or NextCloud instances will be served. We start with no entries here; later, when we set the RDS instance as OAuth2 client for nextcloud, we will add one entry. Later we might want to add another entry form OwnCloud. Each entry will need a `name` that coincides with the domain name in the cloudIds provided by that EFSS, an address and internal address where it can be found, and an OAuth2 client ID and secret for the RDS instance. We will create these later when we deploy and configure the EFSS; essentially, if we uncomment a `global.domains` entry in the provided `values.yaml` file, the only thing we should need to edit are the OAuth2 client ID an secret. More details below.

`layer1-port-zenodo.environment`
: To publish to Zenodo, we need to register our RDS instance as an OAuth2 client for zenodo, and set here the client ID and secret. For development, it is convenient to use [Zenodo's sandbox](https://sandbox.zenodo.org/). To configure it, use `https://test-rds.localdomain.test` as both Website URL and Redirect URI in the OAuth2 form at the Zenodo site (unless you change the `global.rds.domain` value in the `values.yaml` file).

`layer1-port-openscienceframework.environment`
: To publish to OSF, we need to register our RDS instance as an OAuth2 client for OSF, and set here the client ID and secret. For development, it is convenient to use [OSF's test site](https://test.osf.io/dashboard). To configure it, use `https://test-rds.localdomain.test` as both Website URL and Redirect URI (unless you change the `global.rds.domain` value in the `values.yaml` file).

If you decide to not configure either Zenodo of OSF, remember to set its `enabled` flag to false in `values.yaml`, and to comment out the corresponding section.

We can leave the rest of the values as provided.

At this point we can check the minikube IP and add the values of `global.describo.domain` and `global.rds.domain` to `/etc/hosts`, pointing at that IP:

    $ minikube ip
    192.168.49.2

Once we are happy with the `values.yaml` file, and the minikube environment is up,
we are ready to deploy RDS to minikube.

We use the provided script `build-all-dependencies-with-helm.sh` (available at the Sciebo-RDS repo, at path
`/getting-started/minikube-embedded/build-all-dependencies-with-helm.sh`) to build and update the helm charts.
This script is supposed to be run in the same directory where the charts repo is cloned.

    $ cp Sciebo-RDS/getting-started/minikube-embedded/build-all-dependencies-with-helm.sh .
    $ bash build-all-dependencies-with-helm.sh

If this complains about missing Helm repos you may need to add them, e.g. if the nextcloud or owncloud repos are missing:

    $ helm repo add nextcloud https://nextcloud.github.io/helm/
    $ helm repo add owncloud https://owncloud-docker.github.io/helm-charts

And finally we  deploy the RDS stuff to the newly created environment.

    $ helm upgrade -n rds sciebords ./charts/charts/all/ -i --values values.yaml

After a while (a few minutes), the following pods should be up and running:

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


## Setting up NextCloud

We will host the NextCloud instance under `test-nextcloud.localdomain.test`,
so first, in `/etc/hosts`, we point that name to minikube's IP.
Also point `test-rds.localdomain.test` and `test-describo.localdomain.test`
to minikube's IP in `/etc/hosts`.

Now we will install the RDS app into nextcloud.
First we get the software, and build it:

    $ git clone https://github.com/Sciebo-RDS/plugin-nextcloud
    $ cp -R plugin-nextcloud/nextcloud-rds rds
    $ cd rds
    $ make
    $ cd ..
    $ kubectl cp -n rds rds <name of nextcloud pod>:/var/www/html/apps

If the `make` command complains about versions, just remove the `composer.lock` file and run `make` again.

Now you should be able to enable the RDS app in the web interface of NextCloud at `https://test-nextcloud.localdomain.test`
(you will be asked to accept the self signed https certificate for that address)
with an admin account (by default, admin:password): go to `apps` in the menu, and look for it and enable it (you'll need to click twice on "enable").

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

And update the helm release (notice: . refers to the charts git repo)

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

You will need to add exceptions in your browser for the self-signed https certificates for
`test-rds.localdomain.test` and `test-describo.localdomain.test`.

Finally, remember to add an email address to your NextCloud account,
or you won't be authorized to access RDS.

And now you should be able to use RDS from within the NextCloud instance.


## Setting up OwnCloud

We will host the OwnCloud instance under `test-owncloud.localdomain.test`,
so first, in `/etc/hosts`, we point that name to minikube's IP.
Also point `test-rds.localdomain.test` and `test-describo.localdomain.test`
to minikube's IP in `/etc/hosts`.

In OwnCloud, OAuth2 is provided by an app,
so first thing is to enable the OAuth2 app,
via admin settings -> apps,
since the app comes preloaded with OwnCloud.

Now we install the RDS app into owncloud.
It is in the owncloud market, so to install it,
we use the market app (accessible in the top left menu in OwnCloud).
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

You will need to add exceptions in your browser for the self-signed https certificates for
`test-rds.localdomain.test` and `test-describo.localdomain.test`.

Finally, remember to add an email address to your OwnCloud account,
or you won't be authorized to access RDS.

And now you should be able to use RDS from within the OwnCloud instance.


## Development of RDS

If we edit RDS code and want to test it in the minikube environment,
we have to put that code within a docker image,
and update the helm configuration to pick that image.
We edit the code in the Sciebo-RDS cloned repository.

If, for example, we are editing the RDS javascript code, we will want to provide locally the image for the layer0-web pods.
So, from the root of the Sciebo-RDS repo:

    $ cd RDS/layer0_ingress/web/
    $ eval $(minikube -p minikube docker-env)  # this points the current terminal to the minikube docker environment
    $ docker build --build-arg IMAGE_PREFIX="" -f Dockerfile.rds-standalone -t rds-app:0.10 .
    $ docker tag rds-app:0.10 zivgitlab.wwu.io/rds-app:v0.2.4

For the final tag, we may want to replace 0.2.4 with whatever RDS version we are working on.

And now we can configure our values.yaml file to use the built image:

    layer0-web:
      image:
        repository: rds-app
        pullPolicy: Never

And update the helm release (recall: charts is a separate git repo)

    $ helm upgrade -n rds sciebords ./charts/charts/all/ -i --values values.yaml

Note that when you stop the minikube environment with `minikube stop`,
the docker images repo it uses to run the k8s containers is wipped out,
so if you restert the environment, you must rebuild the images that are
local.


## Patching sources

Here I provide a method to rapidly test changes to python code,
simply using `docker cp` to push Python modules into containers.

Note that this method is fairly brittle; as soon as k8s restarts some pod's container,
the patches will be lost. To make the changes more permanent,
they should be added to the images that k8s has available to run its containers,
as described above.
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

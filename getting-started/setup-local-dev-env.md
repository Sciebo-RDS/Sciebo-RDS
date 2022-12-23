# Local install for development using minikube cluster

This guide will help you setup a development environment for developing Research Drive Sciebo Ports on a local Kubernetes cluster on Ubuntu with an owncloud instance.
It should also work on Macosx with minimal changes. If you are running windows as your dev environment, then consider running WSL with Ubuntu as your linux distro.

Prerequisites:
* Python 3.8 < version < 3.10 (Some needed packages and dependencies will only work with these versions. See https://github.com/Sciebo-RDS/connexion-plus/issues/2)
* A running owncloud or nextcloud instance with the RDS plugin installed.

We will take the following steps:

* Setup a local kubernetes cluster with minikube
* Deploy the software to the cluster
* Make RDS web available locally
* Build and run the RDS standalone app
* Mount the RDS directory
* Make the app run on https
* Make a script for easier local setup


## Setup a local kubernetes cluster with minikube
TODO:

* install docker
* install minikube
* install kubectl
* install helm


### Install docker
Follow the instruction on this page: https://docs.docker.com/desktop/install/ubuntu/


### Install minikube

Follow the instruction on this page: https://minikube.sigs.k8s.io/docs/start/
Set the driver to docker:
```sh
minikube config set driver docker
```


### Install kubectl
Follow the instruction on this page: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-using-native-package-management


### Install Helm
Follow the instruction on this page: https://helm.sh/docs/intro/install/#from-apt-debianubuntu


## Deploy the software to the cluster


### Run minikube
Here are the most common commands to get around the minikube cluster:
```sh
minikube delete # will completely remove the cluster
minikube start # will start an existing or new cluster
minikube pause # will pause the current running cluster
kubectl get po -A # will let you see which pods are running
```
Please, also see the minikube.sh script. This has all the needed commands in order.


### Enable ingress
The application uses ingress loadbalancer. This need to be enabled on minikube using following command.

```sh
minikube addons enable ingress
```


### Deploy
To deploy the software to the cluster you need :
* the helm charts
* a values.yaml

To get these, you should only need to follow the instructions on this page: https://www.research-data-services.org/gettingstarted/kubernetes


### Work around
Around the time of this writing [3-11-2022] we need to implement the following workaround to get the application running on the cluster. This workaround is also implemented in the minikube.sh script.

1. Adjust the ingress.yaml for the layer0-describo and layer0-web applications (The latest develop branch already has this change)
2. Do 'helm dep build' on all charts
3. From the getting started folder run helm upgrade

Ad 1.
Line 2 needs to be: 'apiVersion: networking.k8s.io/v1'

Ad 2.
From the minikube.sh script:

```sh
echo "build all dependencies with helm"
cd ./charts
for d in */ ; do
    echo "Going into dir: $d"
    cd "$d"
    echo "Do helm build"
    helm dep build
    cd ..
done
cd ..
```

Ad 3.
Create a namespace first. Then run helm upgrade within that namespace
```sh
kubectl create namespace local-rds
helm upgrade -n local-rds sciebords ../charts/all/ -i --values values.yaml
```


## Make RDS web available locally

The RDS web application will be loaded into an iframe within the owncloud / nextcloud application that has the RDS plugin installed.

We will make the service available by accessing the ingress service through the minikube ip.
Ingress will do all the rerouting. All we need to do is set the domainnames to the minikube ip address in the /etc/hosts file on our system.

In order to make this work we will need to add following line to our host file at /etc/hosts:
```
<minikube ip>  <domainname of the rds web ap>
```
Here is an example of a line that was added to the /etc/hosts:
```sh
192.168.49.2    rds-rd-app-acc.data.surfsara.nl describo-rd-app-acc.data.surfsara.nl
```
To check what domains are configured in ingress run:
```sh
kubectl get ingress -n local-rds|awk '$2 == "nginx" {print $4,$3}'
```


## Build and run the RDS standalone app
We can build the RDS standalone app docker image.
This will ensure that the container will have all the dependencies corresponding to the code we will later mount in the layer0-web service.
From minikube.sh:
```sh
cd ../RDS/layer0_ingress/web
docker build -f ../../../getting-started/Dockerfile.rdsminikube -t rds-standalone:0.10 .
docker tag rds-standalone:0.10 zivgitlab.wwu.io/rds-standalone:v0.1.9
cd ../../..
```

We are tagging the image like this, so we only need to make minimal changes to our values.yaml
We will add below image settings in our values.yaml file.
```yaml
layer0-web: # sciebo rds UI specific options
  image:
    repository: rds-standalone
    # tag: 1.0 # set globally to v0.1.9
    pullPolicy: Never
```


## Mount the RDS directory
We can mount the RDS folder to our minikube instance so we can than mount the folder onto a service.
We do this by adding the following to the minikube start action:
```sh
--mount-string="/home/dave/Projects/Forks/Sciebo-RDS/RDS:/RDS" --mount
```
From minikube.sh:
```sh
minikube start --kubernetes-version=v1.21.0 --mount-string="/home/dave/Projects/Forks/Sciebo-RDS/RDS:/RDS" --mount
```

We can mount the RDS web server code by adding a volume and volumeMount to the deployment.yaml at charts/layer0_web/templates/deployment.yaml.
```yaml
      volumes:
        - name: domainsconfig
          configMap:
            name: domainsconfig
            items:
            - key: domains.json
              path: domains.json
        - name: rds-web-server-storage
          hostPath:
            path: /RDS/layer0_ingress/web/server/src
            type: Directory

      containers:
          volumeMounts:
            - name: rds-web-server-storage
              mountPath: /srv/src
              readOnly: false
            - name: domainsconfig
              mountPath: /srv/domains.json
              subPath: domains.json
              readOnly: true
```


## Make the app run on https
The following commands from minikube.sh will generate a Kubernetes Ingress Controller Fake Certificate:
```sh
echo "#######################################"
echo "create ssl cert for rds-rd-app-acc.data.surfsara.nl"
echo "Change the script to set your domain."
rm -Rf cert
mkdir cert
cd cert
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=rds-rd-app-acc.data.surfsara.nl"
kubectl create secret -n local-rds tls localdomain-rds-tls --key="tls.key" --cert="tls.crt"
kubectl get secret -n local-rds localdomain-rds-tls -o yaml
cd ..
rm -Rf cert
```
In the browser you will manually need to accept the certificate.


## Make a script for easier local setup
You can execute minikube.sh to get up and running. You need to customize the script to your needs and setup.

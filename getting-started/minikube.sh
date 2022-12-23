#!/bin/bash

##############################################
#         RDS minikube development
#
# This script will help you setup a minikube 
# for development of RDS ports
#
# The script will execute all nessecary steps
# to get minikube running and deploy according
# to the values.yaml in the getting-started
# folder.
#
# Simply comment out the steps you want to skip.
##############################################

# echo "######## Making a clean start #########"
# echo "#######################################"
# echo "Stop all docker containers"
# docker container stop $(docker container list -a -q)

# echo "#######################################"
# echo "remove all docker containers"
# docker rm container $(docker container list -a -q)

# echo "#######################################"
# echo "Remove all docker images"
# docker rmi $(docker images -q)

echo "######## Setting up minikube ##########"
echo "#######################################"
echo "start with a new minikube cluster"

echo "#######################################"
echo "Delete the minikube cluster"
minikube delete

echo "#######################################"
echo "Start up a new minikube cluster with kubernetes version 1.21.0"
minikube start --kubernetes-version=v1.21.0 --mount-string="/home/dave/Projects/local-rds/RDS:/RDS" --mount

echo "#######################################"
echo "Set driver to docker"
minikube config set driver docker

echo "#######################################"
echo "Set docker environment to that of minikube, so we can build images directly available in minikube"
eval $(minikube -p minikube docker-env)

echo "#######################################"
echo "Enable the ingress addon"
minikube addons enable ingress

echo "#######################################"
echo "create namespace local-rds in the cluster"
kubectl create ns local-rds

echo "Switching to the root dir"
cd ..

echo "#######################################"
echo "Build the rds standalone image to zivgitlab.wwu.io/rds-standalone:v0.1.9"
cd RDS/layer0_ingress/web
docker build -f ../../../getting-started/Dockerfile.rdsminikube -t rds-standalone:0.10 .
docker tag rds-standalone:0.10 zivgitlab.wwu.io/rds-standalone:v0.1.9
cd ../../..

echo "#######################################"
echo "create ssl cert for rds-rd-app-acc.data.surfsara.nl"
echo "Change the script to set your domain."
rm -Rf cert
mkdir cert
cd cert
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=rds-rd-app-acc.data.surfsara.nl describo-rd-app-acc.data.surfsara.nl"
kubectl create secret -n local-rds tls localdomain-rds-tls --key="tls.key" --cert="tls.crt"
kubectl get secret -n local-rds localdomain-rds-tls -o yaml
cd ..
rm -Rf cert

echo "########## Deploy workaround ##########"
echo "#######################################"
echo "build all dependencies with helm"
cd ./charts
for d in */ ; do
    echo "Going into dir: $d"
    cd "$d"
    echo "Do helm build"
    helm dependency build
    cd ..
done
cd ..

echo "#######################################"
echo "run helm upgrade"
cd getting-started
sleep 60
helm upgrade -n local-rds sciebords ../charts/all/ -i --values values.yaml
cd ..

echo "#######################################"
echo "See cluster status"
echo "kubectl get po -A"
kubectl get po -A

echo "#######################################"
echo "Ingress has been setup like this:"
kubectl get ingress -n local-rds

echo "#######################################"
echo "Set the following in /etc/hosts file:"
echo "$(minikube ip)     <your rds-web domain>"


echo "#### Some handy commands ####"
echo "#######################################"
echo "Forward service on port 80 in the service to port 8000 locally"
echo "kubectl port-forward service/layer0-web -n local-rds 8000:80"

echo "#######################################"
echo "Forward port 8000 to 80"
echo "sudo socat tcp-listen:80,fork tcp:localhost:8000"

echo "#######################################"
echo "Check logs"
echo "kubectl logs -f <POD> -n local-rds"

echo "#######################################"
echo "login to pod"
echo "kubectl exec -it <POD> -n local-rds -- bash"

echo "#######################################"
echo "See what docker image a pod is running on."
echo "kubectl describe -n local-rds pod <POD>  | grep -i image"

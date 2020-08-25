start: install
clean: uninstall

dependencies_ubuntu: dependencies_kubectl_ubuntu dependencies_helm
dependencies_fedora: dependencies_kubectl_fedora dependencies_helm

dependencies_kubectl_ubuntu:
	sudo apt-get update
	sudo apt install -y curl apt-transport-https nano
	curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
	echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
	sudo apt-get update
	sudo apt-get install -y kubectl git

dependencies_kubectl_fedora:
	cat <<EOF > /etc/yum.repos.d/kubernetes.repo
	[kubernetes]
	name=Kubernetes
	baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
	enabled=1
	gpgcheck=1
	repo_gpgcheck=1
	gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
	EOF
	yum install -y kubectl nano git

dependencies_windows:
	choco install -y kubernetes-cli kubernetes-helm minikube nano git
	minikube start

dependencies_helm:
	curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

install_configuration:
	kubectl apply -f configmaps/mserviceurl.yaml
	kubectl apply -f configuration.yaml

uninstall_configuration:
	kubectl delete -f configuration.yaml
	kubectl delete -f configmaps/mserviceurl.yaml

install_namespace:
	kubectl apply -f namespace.yaml

uninstall_namespace:
	kubectl delete -f namespace.yaml

install_tls:
	chmod +x create_certs.sh && ./create_certs.sh

uninstall_tls:
	kubectl delete secret $(sed -n 's/CERT_NAME=\(.*\)/\1/p' < create_certs.sh)

dep_charts:
	helm repo add sciebo-rds https://sciebo-rds.github.io/charts/

upgrade_helm:
	helm upgrade sciebo-rds sciebo-rds/all -i --values values.yaml

install_all: dep_charts upgrade_helm

uninstall_all:
	helm uninstall sciebo-rds
	helm repo remove sciebo-rds

install: install_all
upgrade: upgrade_helm
uninstall: uninstall_all
reinstall: uninstall install

jaeger:
	$(eval POD_JAEGER=$(shell kubectl get pods -l "app.kubernetes.io/name=jaeger,app.kubernetes.io/component=query" -o jsonpath="{.items[0].metadata.name}"))
	echo http://127.0.0.1:8080/
	kubectl port-forward $(POD_JAEGER) 8080:16686

redis:
	$(eval POD_REDIS=$(shell kubectl get pods -l "app.kubernetes.io/name=redis" -o jsonpath="{.items[0].metadata.name}"))
	echo "redis-cli"
	kubectl port-forward $(POD_REDIS) 6379:6379

watch:
	watch -n 1 kubectl get pods -o wide

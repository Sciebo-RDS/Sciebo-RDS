start: install
clean: uninstall

dependencies_ubuntu: dependencies_kubectl_ubuntu dependencies_helm
dependencies_fedora: dependencies_kubectl_fedora dependencies_helm

dependencies_kubectl_ubuntu:
	sudo apt-get update
	sudo apt install -y curl apt-transport-https
	curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
	echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
	sudo apt-get update
	sudo apt-get install -y kubectl

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
	yum install -y kubectl

dependencies_helm:
	curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

install_configmap_mserviceurl:
	kubectl apply -f configmaps/mserviceurl.yaml

remove_configmap_mserviceurl:
	kubectl delete -f configmaps/mserviceurl.yaml

install_kustomization: 
	kubectl apply -k .

uninstall_kustomization:
	kubectl delete -k .

install_configmaps: install_kustomization install_configmap_mserviceurl
uninstall_configmaps: uninstall_kustomization remove_configmap_mserviceurl

install_tls:
	chmod +x create_certs.sh && ./create_certs.sh

uninstall_tls:
	kubectl delete secret sciebords-tls-public

install_all:
	helm upgrade sciebo-rds sciebo-rds/all -i  --values values.yaml
	
uninstall_all:
	helm uninstall sciebo-rds

install: install_configmaps install_all
uninstall: uninstall_all uninstall_configmaps
reinstall: uninstall install

jaeger:
	$(eval POD_JAEGER=$(shell kubectl get pods -l "app.kubernetes.io/instance=jaeger,app.kubernetes.io/component=query" -o jsonpath="{.items[0].metadata.name}"))
	echo http://127.0.0.1:8080/
	kubectl port-forward $(POD_JAEGER) 8080:16686

watch:
	watch -n 1 kubectl get pods -o wide

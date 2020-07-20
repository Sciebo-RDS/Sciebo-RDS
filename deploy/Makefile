all: install

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

port_zenodo:
	helm upgrade circle1-port-zenodo circle1_port_zenodo --install

port_owncloud:
	helm upgrade circle1-port-owncloud circle1_port_owncloud --install

service_exporter:
	helm upgrade circle2-exporter-service circle2_exporter_service --install

service_token:
	helm upgrade circle2-port-service circle2_port_service --install

service_metadata:
	helm upgrade circle2-metadata-service circle2_metadata_service --install

storage_token:
	helm upgrade circle3-token-storage circle3_token_storage --install

storage_research:
	helm upgrade circle3-research-manager circle3_research_manager --install

circle1: port_zenodo port_owncloud
circle2: service_token service_exporter service_metadata
circle3: storage_token storage_research


jaeger:
	helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
	helm repo update
	helm upgrade jaeger jaegertracing/jaeger --install --values jaeger.yaml

remove_jaeger:
	helm uninstall jaeger || true

redis:
	helm install redis bitnami/redis-cluster --values redis.yaml

remove_redis:
	helm uninstall redis || true

features: jaeger redis

remove_features: remove_jaeger remove_redis

remove_port_zenodo:
	helm uninstall circle1-port-zenodo || true

remove_port_owncloud:
	helm uninstall circle1-port-owncloud || true

remove_service_exporter:
	helm uninstall circle2-exporter-service || true

remove_service_token:
	helm uninstall circle2-port-service || true

remove_service_metadata:
	helm uninstall circle2-metadata-service || true

remove_storage_token:
	helm uninstall circle3-token-storage || true

remove_storage_research:
	helm uninstall circle3-research-manager || true

uninstall_circle1: remove_port_zenodo remove_port_owncloud
uninstall_circle2: remove_service_token remove_service_exporter remove_service_metadata
uninstall_circle3: remove_storage_token remove_storage_research

install_tls:
	chmod +x create_certs.sh && ./create_certs.sh

uninstall_tls:
	kubectl delete secret sciebords-tls-public

install: install_configmaps features circle3 circle2 circle1
uninstall: uninstall_circle1 uninstall_circle2 uninstall_circle3 remove_features uninstall_configmaps
clean: uninstall
reinstall: uninstall install
reinstall_fast: uninstall_circle1 uninstall_circle2 uninstall_circle3 install_configmaps circle3 circle2 circle1

jaeger:
	$(eval POD_JAEGER=$(shell kubectl get pods --namespace sciebo-rds -l "app.kubernetes.io/instance=jaeger,app.kubernetes.io/component=query" -o jsonpath="{.items[0].metadata.name}"))
	echo http://127.0.0.1:8080/
	kubectl port-forward --namespace sciebo-rds $(POD_JAEGER) 8080:16686

watch:
	watch -n 1 kubectl get pods -o wide

install_configmap_proxy:
	kubectl apply -f configmaps/httpproxy.yaml

install_configmap_mserviceurl:
	kubectl apply -f configmaps/mserviceurl.yaml

remove_configmap_proxy:
	kubectl delete -f configmaps/httpproxy.yaml

remove_configmap_mserviceurl:
	kubectl delete -f configmaps/mserviceurl.yaml

install_configmaps: install_configmap_proxy install_configmap_mserviceurl
uninstall_configmaps: remove_configmap_mserviceurl remove_configmap_proxy

port_zenodo:
	helm upgrade circle1-port-zenodo circle1_port_zenodo --install

port_owncloud:
	helm upgrade circle1-port-owncloud circle1_port_owncloud --install

service_exporter:
	helm upgrade circle2-exporter-service circle2_exporter_service --install

service_token:
	helm upgrade circle2-token-service circle2_token_service --install

service_metadata:
	helm upgrade circle2-metadata-service circle2_metadata_service --install

storage_token:
	helm upgrade circle3-token-storage circle3_token_storage --install

storage_research:
	helm upgrade circle3-research-manager circle3_research_manager --install

circle1: port_zenodo port_owncloud
circle2: service_token service_exporter service_metadata
circle3: storage_token storage_research

features:
	helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
	helm repo update
	helm upgrade jaeger jaegertracing/jaeger --install --values jaeger.yaml

remove_features:
	helm delete --purge jaeger || true

remove_port_zenodo:
	helm delete --purge circle1-port-zenodo || true

remove_port_owncloud:
	helm delete --purge circle1-port-owncloud || true

remove_service_exporter:
	helm delete --purge circle2-exporter-service || true

remove_service_token:
	helm delete --purge circle2-token-service || true

remove_service_metadata:
	helm delete --purge circle2-metadata-service || true

remove_storage_token:
	helm delete --purge circle3-token-storage || true

remove_storage_research:
	helm delete --purge circle3-research-manager || true

uninstall_circle1: remove_port_zenodo remove_port_owncloud
uninstall_circle2: remove_service_token remove_service_exporter remove_service_metadata
uninstall_circle3: remove_storage_token remove_storage_research

install: install_configmaps features circle3 circle2 circle1
uninstall: uninstall_circle1 uninstall_circle2 uninstall_circle3 remove_features uninstall_configmaps
clean: uninstall
reinstall: uninstall install
reinstall_fast: uninstall_circle1 uninstall_circle2 uninstall_circle3 circle3 circle2 circle1

jaeger:
	$(eval POD_JAEGER=$(shell kubectl get pods --namespace sciebo-rds -l "app.kubernetes.io/instance=jaeger,app.kubernetes.io/component=query" -o jsonpath="{.items[0].metadata.name}"))
	echo http://127.0.0.1:8080/
	kubectl port-forward --namespace sciebo-rds $(POD_JAEGER) 8080:16686

port_zenodo:
	helm upgrade circle1-port-zenodo circle1_port_zenodo --install

token_service:
	helm upgrade circle2-token-service circle2_token_service --install

token_storage:
	helm upgrade circle3-token-storage circle3_token_storage --install

circle1: port_zenodo
circle2: token_service
circle3: token_storage

remove_port_zenodo:
	helm delete --purge circle1-port-zenodo || true

remove_token_service:
	helm delete --purge circle2-token-service || true

remove_token_storage:
	helm delete --purge circle3-token-storage || true

uninstall_circle1: remove_port_zenodo
uninstall_circle2: remove_token_service
uninstall_circle3: remove_token_storage

install: circle1 circle2 circle3
uninstall: uninstall_circle1 uninstall_circle2 uninstall_circle3

port_zenodo:
	helm upgrade -i port-zenodo ./circle1_port_zenodo

token_service:
	helm upgrade -i circle2-token-service ./circle2_token_service

token_storage:
	helm upgrade -i circle3-token-service ./circle2_token_service

circle1: port_zenodo

circle2: token_service

circle3: token_storage

install: circle1 circle2 circle3
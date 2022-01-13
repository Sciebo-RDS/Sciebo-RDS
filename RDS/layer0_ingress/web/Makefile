ifneq (,$(wildcard ./.env))
    include .env
    export
endif

ubuntu:
	sudo apt install -y curl unzip

fedora:
	sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
	sudo yum install -y curl unzip yum-utils docker-ce docker-ce-cli containerd.io

install:
	apt install gettext
	cd client
	npm install -g yarn
	yarn --cwd ./client install
	ln -s ../../client/node_modules packages/codebase/node_modules

l10n-compile:
	yarn --cwd ./client localize-compile 
	
l10n-extract:
	yarn --cwd ./client localize-extract

flask:
	cd server
	pipenv shell
	FLASK_APP=starter.py flask run

socket:
	cd server && pipenv run python websocket.py

lint:
	npm --prefix ./client run lint
	pipenv run black .

build:
	yarn --cwd ./client workspaces build

test:
	yarn --cwd ./client test && cd server && cd server && pipenv run pytest

web: describo
	yarn --cwd ./client install
	docker-compose -f client/dev/docker-compose.yml up -d
	tmux new-session -d -s ocis "yarn --cwd ./client/dev/web install && yarn --cwd ./client/dev/web serve"\;\
		 split-window -h "yarn --cwd ./client workspace @rds/web serve" || true
	tmux new-session -d -s standalone "cd client && while true; do yarn serve; done" \; split-window -h "cd server && while true; do pipenv run python starter.py; done" \; || true
	@while [ $(shell curl  -sw '%{http_code}' localhost:8000) -gt 302 ]; do true; done;
	@docker exec -it owncloud_server /bin/bash -c "cat config.php > config/config.php"
	@docker exec -it owncloud_server /bin/bash -c "occ user:modify admin email not@valid.tld"
	@docker exec -it owncloud_server /bin/bash -c "occ app:enable oauth2 && occ app:enable rds"
	@docker exec -it owncloud_server /bin/bash -c "occ oauth2:add-client web AfRGQ5ywVhNQDlfGVbntjDOn2rLPTjg0SYEVBlvuYV4UrtDmmgIvKWktIMDP5Dqq WnxAqddPtPzX3lyCYijHi3pVs1HGpoumzTYSUWqrVfL0vT7E92JSzNTQABBzCaIm http://localhost:9100/oidc-callback.html | true"
	@echo "Open http://localhost:9100 with your browser."
	@echo 'If you want to close the server, execute "make stop" and close everything.'

ocis:
	@echo "This is currently not tested!"
	@echo "Cancel with ctrl+c"
	@sleep 5
	tmux new-session -d -s ocis "cd client/dev/ocis/ocis && OCIS_LOG_PRETTY=true OCIS_LOG_COLOR=true OCIS_LOG_LEVEL=DEBUG go run cmd/ocis/main.go server"\;\
		 split-window -h "yarn --cwd ./client/dev/web serve"\;\
		 split-window -h "yarn --cwd ./client workspace @rds/web serve"
	tmux new-session -d -s standalone "cd client && while true; do yarn serve; done" \; split-window -h "cd server && while true; do pipenv run python starter.py; done" \; || test
	@echo "Wait 20s for server startup to kill web"
	@sleep 20
	tmux new-session -d "cd client/dev/ocis/ocis && go run cmd/ocis/main.go kill web"
	@echo "Done. Open http://localhost:9200 with your browser."
	@echo 'If you want to close the server, execute "make stop" and close everything.'

classic: describo
	yarn --cwd ./client install
	yarn --cwd ./client classic
	echo '$$(function () {' > ./client/packages/classic/php/js/app.js
	cat ./client/packages/classic/dist/js/app.js >> ./client/packages/classic/php/js/app.js
	echo "});" >> ./client/packages/classic/php/js/app.js
	docker-compose -f client/dev/docker-compose.yml up -d
	tmux new-session -d -s standalone "cd client && while true; do yarn serve; done" \; split-window -h "cd server && while true; do pipenv run python starter.py; done" \; || true
	@echo Wait for 20 Seconds to boot everything up.
	while [ $(shell curl  -sw '%{http_code}' localhost:8000) -gt 302 ]; do true; done;
	@docker exec -it owncloud_server /bin/bash -c "occ user:modify admin email not@valid.tld"
	@docker exec -it owncloud_server /bin/bash -c "occ app:enable oauth2 && occ app:enable rds"
	@docker exec -it owncloud_server /bin/bash -c "occ oauth2:add-client describo AfRGQ5ywVhNQDlfGVbntjDOn2rLPTjg0SYEVBlvuYV4UrtDmmgIvKWktIMDP5Dqq WnxAqddPtPzX3lyCYijHi3pVs1HGpoumzTYSUWqrVfL0vT7E92JSzNTQABBzCaIm ${OWNCLOUD_URL}/apps/describo/authorize"
	@docker exec -it owncloud_server /bin/bash -c "occ rds:set-oauthname web && occ rds:set-url ${RDS_URL}"
	@docker exec -it owncloud_server /bin/bash -c "occ oauth2:add-client web AfRGQ5ywVhNQDlfGVbntjDOn2rLPTjg0SYEVBlvuYV4UrtDmmgIvKWktIMDP5Dqq WnxAqddPtPzX3lyCYijHi3pVs1HGpoumzTYSUWqrVfL0vT7E92JSzNTQABBzCaIm http://localhost:9100/oidc-callback.html | true"
	@echo Warning!!! You have to create a new oauth2 url and enter it in root .env file and configure RDS properly.
	@echo Start on http://localhost:8000

standalone: describo
	docker-compose -f client/dev/docker-compose.yml up -d
	tmux new-session -d -s standalone "cd client && while true; do yarn serve; done" \; split-window -h "cd server && while true; do pipenv run python starter.py; done" \;
	@echo Wait for 20 Seconds to boot everything up.
	@sleep 20
	@docker exec -it owncloud_server /bin/bash -c "occ app:enable oauth2 && occ app:enable rds"
	@echo Warning!!! You have to create a new oauth2 url and enter it in root .env file and configure RDS properly.
	@echo Start on http://localhost:8000

describo:
	docker-compose -f client/dev/describo-online/docker-compose.yml up -d

stop:
	docker-compose -f client/dev/docker-compose.yml down || true
	docker-compose -f client/dev/describo-online/docker-compose.yml down || true
	tmux kill-session -t ocis || true
	tmux kill-session -t classic || true
	tmux kill-session -t standalone || true
	sudo chown -R $(shell id -un):$(shell id -gn) client

start:
	docker-compose -f setup/docker-compose.yml --env-file .env up -d

CONFIG = $$CONFIG
setup-install: setup
	@echo "Not for production use!!! Or remove the oauth2 client by hand and create a new one and set all informations in docker-compose.yml"
	@echo "Wait for ownCloud installation completion."
	@while [ $(shell curl  -sw '%{http_code}' localhost) -gt 302 ]; do true; done;
	@docker exec -it owncloud_server /bin/bash -c "head -n -1 config/config.php > config.php"
	@docker exec -it owncloud_server /bin/bash -c "echo \"'web.baseUrl' => 'http://${OWNCLOUD_DOMAIN}/web', 'cors.allowed-domains' => ['http://${OWNCLOUD_DOMAIN}:9100','http://${OWNCLOUD_DOMAIN}:8008'],);\" >> config.php"
	@docker exec -it owncloud_server /bin/bash -c "cp config.php config/config.php"
	@docker exec -it owncloud_server /bin/bash -c "occ user:modify admin email ${ADMIN_MAIL}"
	@docker exec -it owncloud_server /bin/bash -c "occ market:install oauth2 && occ market:install web && occ app:enable oauth2 && occ app:enable rds"
	@docker exec -it owncloud_server /bin/bash -c "occ rds:set-oauthname web && occ rds:set-url ${RDS_URL}"
	@docker exec -it owncloud_server /bin/bash -c "occ oauth2:add-client web ${OWNCLOUD_OAUTH2_CLIENT_ID} ${OWNCLOUD_OAUTH2_CLIENT_SECRET} ${OWNCLOUD_OAUTH_CLIENT_REDIRECT}"
	
setup-build:
	docker-compose -f setup/docker-compose.yml --env-file .env up -d --build

setup-stop:
	docker-compose -f setup/docker-compose.yml --env-file .env down
	docker-compose -f client/dev/describo-online/docker-compose.yml down || true

clean:
	docker-compose -f setup/docker-compose.yml --env-file .env down --rmi all --volumes --remove-orphans 

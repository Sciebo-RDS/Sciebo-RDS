SHELL := /bin/bash

define SNIPPET
Add the following code snippet to external_apps in web/config.json:

{
	"id": "hello-world",
	"path": "http://localhost:8082/index.js"
}'
endef

define NVM_SNIPPET
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
endef


install: installgo installnpm
	apt install tmux git

	git clone https://github.com/owncloud/ocis.git
	git clone https://github.com/owncloud/web.git

	yarn --cwd web install

	echo -e '${SNIPPET}'

installgo:
	wget https://golang.org/dl/go1.16.2.linux-amd64.tar.gz
	tar -C /usr/local -xzf go1.16.2.linux-amd64.tar.gz
	echo 'export PATH=$PATH:/usr/local/go/bin' >> $(HOME)/.bashrc

installnpm:
	curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
	$(HOME)/.nvm/nvm.sh install --lts
	npm install -g yarn
	echo '${NVM_SNIPPET}' >> $(HOME)/.bashrc

start:
	npm version
	$(HOME)/.nvm/nvm.sh use --lts
	$(HOME)/.nvm/nvm.sh alias default lts/fermium
	@tmux new-session -d -s ocis "cd ocis/ocis && OCIS_LOG_PRETTY=true OCIS_LOG_COLOR=true OCIS_LOG_LEVEL=DEBUG go run cmd/ocis/main.go server"\;\
		 split-window -h "yarn --cwd web serve"\;\
		 split-window -h "yarn --cwd extension serve"
	@echo "Wait 20s for server startup to kill web"
	@sleep 20
	@tmux new-session -d "cd ocis/ocis && go run cmd/ocis/main.go kill web"
	@echo "Done. Open https://localhost:9200 with your browser."
	@echo 'If you want to close the server, execute "make stop" and close everything.'

stop:
	tmux kill-session -t ocis
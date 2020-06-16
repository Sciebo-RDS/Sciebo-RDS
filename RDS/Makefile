
update:
	for circle in $$(ls -d */) ; \
	do \
		echo "$$circle" ; \
		cd $(shell pwd)/$$circle ; \
		for svc in $$(ls -d */) ; do \
			echo "$$svc" ; \
			cd $(shell pwd)/$$circle/$$svc ; \
			make update ; \
		done ; \
	done


pipenv-install:
	for circle in $$(ls -d */) ; \
	do \
		echo "$$circle" ; \
		cd $(shell pwd)/$$circle ; \
		for svc in $$(ls -d */) ; do \
			echo "$$svc" ; \
			cd $(shell pwd)/$$circle/$$svc ; \
			pipenv install --dev; \
		done ; \
	done



test:
	for circle in $$(ls -d */) ; \
	do \
		echo "$$circle" ; \
		cd $(shell pwd)/$$circle ; \
		for svc in $$(ls -d */) ; do \
			echo "$$svc" ; \
			cd $(shell pwd)/$$circle/$$svc ; \
			make test ; \
		done ; \
	done

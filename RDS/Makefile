
update:
	for circle in $$(ls -d */) ; \
	do \
		echo "$$circle" ; \
		cd $(shell pwd)/$$circle ; \
		for svc in $$(ls -d */) ; do \
			cd $(shell pwd)/$$circle/$$svc ; \
			make update ; \
		done ; \
	done

# updates the pipfiles
install:
	@pipenv shell > /dev/null 2>&1 || true
	@pip install -r requirements.txt | grep -v 'already satisfied' || true

dev: install
	@pip install -r requirements-dev.txt | grep -v 'already satisfied' || true

update:
	pipenv update
	pipenv lock -r > requirements.txt
	pipenv lock -r -d > requirements-dev.txt

test: dev
	python -m pytest

run: install
	python src/server.py

loc: dev
	@pygount --suffix=py src | cut -f 1 | awk '{s+=$$1} END {print "Source " s}'
	@pygount --suffix=py tests | cut -f 1 | awk '{s+=$$1} END {print "Tests " s}'
	@pygount --suffix=py | cut -f 1 | awk '{s+=$$1} END {print "All " s}'

doc: dev
	pydocmd build
	mv _build/pydocmd/project.md ../../../docs/content/doc/impl/central/project-service-docstring.md
	rm -r _build



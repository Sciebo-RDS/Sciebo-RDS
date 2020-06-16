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
	@#docker run -d --network host --privileged --name server docker.io/selenium/standalone-firefox || true
	python -m pytest --cov=src
	@#docker stop server || true

run: install
	python src/server.py

loc: dev
	@pygount --suffix=py src | cut -f 1 | awk '{s+=$$1} END {print "Source " s}'
	@pygount --suffix=py tests | cut -f 1 | awk '{s+=$$1} END {print "Tests " s}'
	@pygount --suffix=py | cut -f 1 | awk '{s+=$$1} END {print "All " s}'

doc: dev
	pydocmd build
	mv _build/pydocmd/exporter.md ../../../docs/content/doc/impl/use-cases/exporter-service-docstring.md
	rm -r _build



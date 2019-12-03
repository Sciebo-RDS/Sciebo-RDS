# updates the pipfiles
install:
	pipenv shell || true
	pip install -r requirements.txt

dev: install
	pip install -r requirements-dev.txt

update:
	pipenv update
	pipenv lock -r > requirements.txt
	pipenv lock -r -d > requirements-dev.txt

test: dev
	python -m pytest

run: install
	python src/server.py

loc: dev
	pygount --suffix=py | cut -f 1 | awk '{s+=$$1} END {print s}'

doc: dev
	pydocmd build
	mv _build/pydocmd/token-service.md ../../../docs/content/doc/impl/central/token-service-docstring.md
	rm -r _build



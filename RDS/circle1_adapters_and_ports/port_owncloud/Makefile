# updates the pipfiles
install:
	pipenv shell || true
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

update:
	pipenv update
	pipenv lock -r > requirements.txt
	pipenv lock -r -d > requirements-dev.txt

test:
	python -m pytest --cov=src

run:
	python src/server.py
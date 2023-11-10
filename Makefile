.PHONY: activate
activate:
	. .venv/bin/activate

.PHONY: setup-env
setup-env:
	python -m venv .venv

.PHONY: setup
setup: setup-env activate
	python -m pip install -r requirements.txt

.PHONY: gen-reqs
gen-reqs: activate
	python -m pip freeze > requirements.txt

.PHONY: clean
clean:
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf .mypy_cache
	rm -rf .tox
	rm -rf .eggs
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

.PHONY: g-install
g-install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

.PHONY: black
black: activate
	python -m black .

.PHONY: ruff
ruff: activate
	python -m ruff .



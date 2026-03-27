PYTHON := .venv/bin/python
PIP := .venv/bin/pip
FLASK := .venv/bin/flask

.PHONY: dev install migrate test

dev:
	$(PYTHON) run.py

install:
	$(PIP) install -r requirements.txt

migrate:
	$(FLASK) db upgrade

test:
	$(PYTHON) -m pytest -q

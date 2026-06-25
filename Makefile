VENV ?= .venv
VENV_PATH := $(CURDIR)/$(VENV)
PYTHON ?= $(VENV_PATH)/bin/python
GRADLE ?= gradle

.PHONY: install lint test test-epoch test-now build up down integration ci

$(PYTHON):
	python3 -m venv $(VENV)

install: $(PYTHON)
	$(PYTHON) -m pip install -r services/epoch-service/requirements-dev.txt

lint: install
	cd services/epoch-service && $(PYTHON) -m ruff format --check .
	cd services/epoch-service && $(PYTHON) -m ruff check .

test: lint test-epoch test-now

test-epoch: install
	cd services/epoch-service && $(PYTHON) -m pytest

test-now:
	cd services/now-time-service && $(GRADLE) --no-daemon test

build:
	docker compose build

up:
	docker compose up --build

down:
	docker compose down --remove-orphans

integration: install
	@set -e; \
	docker compose up -d --build; \
	trap 'docker compose down --remove-orphans' EXIT; \
	$(PYTHON) -m pytest tests/integration

ci: test build integration

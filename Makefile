.PHONY: backend-dev backend-lint backend-install backend-venv

PYTHON ?= python
BACKEND_DIR := apps/backend
ENV_FILE ?= .env

backend-dev:
	cd $(BACKEND_DIR) && $(PYTHON) -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 --env-file ../../$(ENV_FILE)

backend-lint:
	cd $(BACKEND_DIR) && ruff check

backend-install:
	$(PYTHON) -m pip install -r requirements.txt

backend-venv:
	$(PYTHON) -m venv .venv

.PHONY: backend-dev backend-lint backend-install backend-venv

PYTHON ?= python
BACKEND_DIR := apps/backend
ENV_FILE ?= .env

# Determine an env file argument only if the file exists to avoid uvicorn errors.
ENV_FILE_ARG :=
ifneq (,$(wildcard $(ENV_FILE)))
ENV_FILE_ARG := --env-file $(ENV_FILE)
else ifneq (,$(wildcard $(BACKEND_DIR)/.env))
ENV_FILE_ARG := --env-file $(BACKEND_DIR)/.env
endif

backend-dev:
	$(PYTHON) -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 $(ENV_FILE_ARG)

backend-lint:
	cd $(BACKEND_DIR) && ruff check

backend-install:
	$(PYTHON) -m pip install -r requirements.txt

backend-venv:
	$(PYTHON) -m venv .venv

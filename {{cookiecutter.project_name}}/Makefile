.DEFAULT_GOAL := help

PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
SRC_DIR ?= src
TEST_DIR ?= tests
COVERAGE_MIN ?= 90
COMPOSE ?= docker compose
SERVICES ?=

.PHONY: help venv install format format-check lint test coverage tox build clean ci compose-up compose-down compose-logs compose-build compose-ps

help:
	@echo "Targets:"
	@echo "  venv          Create a virtual environment at .venv"
	@echo "  install       Install project in editable mode with dev extras"
	@echo "  format        Format code with black"
	@echo "  format-check  Check formatting with black --check"
	@echo "  lint          Run black --check and flake8"
	@echo "  test          Run pytest"
	@echo "  coverage      Run pytest with coverage (min $(COVERAGE_MIN)%)"
	@echo "  tox           Run tox across environments"
	@echo "  build         Build sdist and wheel into dist/"
	@echo "  clean         Remove build/test caches"
	@echo "  compose-up    Start docker compose services (SERVICES=\"\")"
	@echo "               Use SERVICES to select which services to run."
	@echo "               Example: make compose-up SERVICES=\"web worker\""
	@echo "               Example: make compose-up SERVICES=redis"
	@echo "               SERVICES=\"\" (default) starts all services."
	@echo "  compose-down  Stop docker compose services"
	@echo "  compose-logs  Tail docker compose logs (SERVICES=\"\")"
	@echo "               Use SERVICES to select which services to tail."
	@echo "               Example: make compose-logs SERVICES=web"
	@echo "  compose-build Build docker compose services (SERVICES=\"\")"
	@echo "               Use SERVICES to select which services to build."
	@echo "               Example: make compose-build SERVICES=\"web worker\""
	@echo "  compose-ps    Show docker compose status"
	@echo "  ci            Run format-check, lint, coverage, tox"

venv:
	$(PYTHON) -m venv .venv

install:
	$(PIP) install -e ".[dev,server,tasks]"

format:
	$(PYTHON) -m black $(SRC_DIR) $(TEST_DIR)

format-check:
	$(PYTHON) -m black --check $(SRC_DIR) $(TEST_DIR)

lint: format-check
	$(PYTHON) -m flake8 $(SRC_DIR) $(TEST_DIR)

test:
	DJANGO_SETTINGS_MODULE={{ cookiecutter.project_slug|replace('-', '_') }}.server.settings \
	CELERY_TASK_ALWAYS_EAGER=1 \
	CELERY_TASK_EAGER_PROPAGATES=1 \
	$(PYTHON) -m pytest $(TEST_DIR)

coverage:
	DJANGO_SETTINGS_MODULE={{ cookiecutter.project_slug|replace('-', '_') }}.server.settings \
	CELERY_TASK_ALWAYS_EAGER=1 \
	CELERY_TASK_EAGER_PROPAGATES=1 \
	$(PYTHON) -m pytest --cov={{ cookiecutter.project_slug|replace('-', '_') }} --cov-report=term-missing --cov-fail-under=$(COVERAGE_MIN)

tox:
	$(PYTHON) -m tox

build:
	$(PYTHON) -m pip install -U build
	$(PYTHON) -m build

clean:
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov dist build .eggs .tox
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.egg" -exec rm -f {} +
	find . -type f \( -name "*.pyc" -o -name "*.pyo" -o -name "*.pyd" \) -exec rm -f {} +

compose-up:
	$(COMPOSE) up -d $(SERVICES)

compose-down:
	$(COMPOSE) down

compose-logs:
	$(COMPOSE) logs -f $(SERVICES)

compose-build:
	$(COMPOSE) build $(SERVICES)

compose-ps:
	$(COMPOSE) ps

ci: format-check lint coverage tox

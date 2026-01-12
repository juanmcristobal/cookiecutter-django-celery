# {{ cookiecutter.project_name }}

Minimal, production-minded Django + Celery backend with a single Python namespace: `{{ cookiecutter.package_name }}`.
Requires Python {{ cookiecutter.python_version }}+.

## Quick Start (local)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,server,tasks]"
```

Run web (WSGI):
```bash
{{ cookiecutter.project_slug }}-manage runserver
```

Run web (ASGI):
```bash
uvicorn {{ cookiecutter.package_name }}.server.asgi:application --host 0.0.0.0 --port 8000
```

Run worker and beat:
```bash
{{ cookiecutter.project_slug }}-celery worker -l info
{{ cookiecutter.project_slug }}-celery beat -l info
```

Celery Beat schedule is configured in `{{ cookiecutter.package_name }}.server.settings` via `CELERY_BEAT_SCHEDULE`.

Health check:
```bash
curl http://localhost:8000/api/health/
```

## Docker (dev)

```bash
cp .env.example .env
docker compose up --build
```

## Tests and Lint

```bash
pytest
ruff check src tests
mypy src
```

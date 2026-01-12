import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "{{ cookiecutter.project_slug|replace('-', '_') }}.server.settings",
)

from celery import Celery  # noqa: E402

app = Celery("{{ cookiecutter.project_slug|replace('-', '_') }}")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["{{ cookiecutter.project_slug|replace('-', '_') }}.core"], force=True)

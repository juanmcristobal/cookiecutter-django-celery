import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "{{ cookiecutter.package_name }}.server.settings",
)

from celery import Celery  # noqa: E402

app = Celery("{{ cookiecutter.package_name }}")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["{{ cookiecutter.package_name }}.core"], force=True)

import os

import django
from django.test import Client


def test_smoke_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "{{ cookiecutter.package_name }}.server.settings",
    )
    django.setup()

    client = Client()
    response = client.get("/api/health/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

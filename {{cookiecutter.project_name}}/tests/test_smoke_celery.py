import os


def test_smoke_celery():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "{{ cookiecutter.project_slug|replace('-', '_') }}.server.settings",
    )
    os.environ.setdefault("CELERY_TASK_ALWAYS_EAGER", "1")
    os.environ.setdefault("CELERY_TASK_EAGER_PROPAGATES", "1")

    import django

    django.setup()

    from {{ cookiecutter.project_slug|replace('-', '_') }}.tasks.celery_app import app

    assert app is not None

    registered_tasks = list(app.tasks.keys())
    assert "{{ cookiecutter.project_slug|replace('-', '_') }}.core.tasks.ping" in registered_tasks
    assert "{{ cookiecutter.project_slug|replace('-', '_') }}.core.tasks.add" in registered_tasks

    result = app.tasks["{{ cookiecutter.project_slug|replace('-', '_') }}.core.tasks.ping"].apply().get(
        timeout=10
    )
    assert result == "pong"

    result = (
        app.tasks["{{ cookiecutter.project_slug|replace('-', '_') }}.core.tasks.add"]
        .apply(args=(2, 3))
        .get(timeout=10)
    )
    assert result == 5

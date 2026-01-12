import os
import sys


def test_manage_cli_invokes_execute(monkeypatch):
    from {{ cookiecutter.package_name }} import manage_cli

    captured = {}

    def fake_execute(argv):
        captured["argv"] = argv

    monkeypatch.setattr(
        "django.core.management.execute_from_command_line", fake_execute
    )
    monkeypatch.setattr(sys, "argv", ["{{ cookiecutter.project_slug }}-manage", "check"])
    monkeypatch.delenv("DJANGO_SETTINGS_MODULE", raising=False)

    manage_cli.main()

    assert (
        os.environ["DJANGO_SETTINGS_MODULE"]
        == "{{ cookiecutter.package_name }}.server.settings"
    )
    assert captured["argv"] == ["{{ cookiecutter.project_slug }}-manage", "check"]


def test_tasks_cli_injects_app(monkeypatch):
    from {{ cookiecutter.package_name }}.tasks import cli

    captured = {}

    def fake_main():
        captured["argv"] = sys.argv[:]

    monkeypatch.setattr(cli, "celery_main", fake_main)
    monkeypatch.setattr(
        sys,
        "argv",
        ["{{ cookiecutter.project_slug }}-celery", "worker", "-l", "info"],
    )
    monkeypatch.delenv("DJANGO_SETTINGS_MODULE", raising=False)

    cli.main()

    assert (
        os.environ["DJANGO_SETTINGS_MODULE"]
        == "{{ cookiecutter.package_name }}.server.settings"
    )
    assert captured["argv"] == [
        "celery",
        "-A",
        "{{ cookiecutter.package_name }}.tasks.celery_app",
        "worker",
        "-l",
        "info",
    ]


def test_tasks_cli_respects_app_arg(monkeypatch):
    from {{ cookiecutter.package_name }}.tasks import cli

    captured = {}

    def fake_main():
        captured["argv"] = sys.argv[:]

    monkeypatch.setattr(cli, "celery_main", fake_main)
    monkeypatch.setattr(
        sys,
        "argv",
        ["{{ cookiecutter.project_slug }}-celery", "-A", "custom.app", "worker"],
    )

    cli.main()

    assert captured["argv"] == ["celery", "-A", "custom.app", "worker"]


def test_wsgi_application():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "{{ cookiecutter.package_name }}.server.settings",
    )

    from {{ cookiecutter.package_name }}.server import wsgi

    assert wsgi.application is not None


def test_asgi_application():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "{{ cookiecutter.package_name }}.server.settings",
    )

    from {{ cookiecutter.package_name }}.server import asgi

    assert asgi.application is not None

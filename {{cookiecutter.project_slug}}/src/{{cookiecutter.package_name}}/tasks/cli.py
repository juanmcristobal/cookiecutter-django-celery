import os
import sys

from celery.bin.celery import main as celery_main


def _has_app_arg(argv):
    if "-A" in argv or "--app" in argv:
        return True
    return any(arg.startswith("--app=") for arg in argv)


def main():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "{{ cookiecutter.package_name }}.server.settings",
    )
    argv = sys.argv[1:]
    if not _has_app_arg(argv):
        argv = ["-A", "{{ cookiecutter.package_name }}.tasks.celery_app"] + argv
    sys.argv = ["celery"] + argv
    celery_main()

from celery import shared_task


@shared_task(name="{{ cookiecutter.project_slug|replace('-', '_') }}.core.tasks.ping", queue="high")
def ping():
    return "pong"


@shared_task(name="{{ cookiecutter.project_slug|replace('-', '_') }}.core.tasks.add", queue="default")
def add(a, b):
    return a + b

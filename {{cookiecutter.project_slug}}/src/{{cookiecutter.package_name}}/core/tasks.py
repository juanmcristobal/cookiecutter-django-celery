from celery import shared_task


@shared_task(name="{{ cookiecutter.package_name }}.core.tasks.ping", queue="high")
def ping():
    return "pong"


@shared_task(name="{{ cookiecutter.package_name }}.core.tasks.add", queue="default")
def add(a, b):
    return a + b

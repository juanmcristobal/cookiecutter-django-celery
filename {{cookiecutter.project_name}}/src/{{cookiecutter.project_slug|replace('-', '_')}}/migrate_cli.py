import os

import click


@click.command(
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True}
)
@click.pass_context
def main(ctx):
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "{{ cookiecutter.project_slug|replace('-', '_') }}.server.settings",
    )
    from django.core.management import execute_from_command_line

    execute_from_command_line(["django-admin", "migrate", *ctx.args])

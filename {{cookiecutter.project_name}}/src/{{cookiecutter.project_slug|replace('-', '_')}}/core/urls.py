from django.urls import path

from {{ cookiecutter.project_slug|replace('-', '_') }}.core.views import health

urlpatterns = [
    path("health/", health),
]

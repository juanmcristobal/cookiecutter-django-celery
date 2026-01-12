from django.urls import path

from {{ cookiecutter.package_name }}.core.views import health

urlpatterns = [
    path("health/", health),
]

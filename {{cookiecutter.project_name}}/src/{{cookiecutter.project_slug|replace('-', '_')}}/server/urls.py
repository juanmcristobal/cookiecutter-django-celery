from django.urls import include, path

urlpatterns = [
    path("api/", include("{{ cookiecutter.project_slug|replace('-', '_') }}.core.urls")),
]

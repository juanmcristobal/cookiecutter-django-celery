from django.urls import include, path

urlpatterns = [
    path("api/", include("{{ cookiecutter.package_name }}.core.urls")),
]

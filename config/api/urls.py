"""Top-level API URL configuration."""

from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("v1/", include("config.api.v1.urls")),
]

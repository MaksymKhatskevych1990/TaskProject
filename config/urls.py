"""Root URL configuration."""

from django.contrib import admin
from django.urls import include, path

from apps.common.api import urls as health_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "health/",
        include(
            (health_urls.urlpatterns, health_urls.app_name),
            namespace="health",
        ),
    ),
    path(
        "api/health/",
        include(
            (health_urls.urlpatterns, health_urls.app_name),
            namespace="legacy-health",
        ),
    ),
    path("api/", include("config.api.urls")),
]

"""Central registry for version 1 API endpoints."""

from django.urls import include, path

from apps.accounts.api.auth import (
    LogoutView,
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "v1"

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/logout/", LogoutView.as_view(), name="token-logout"),
    path("accounts/", include("apps.accounts.api.urls")),
    path("employees/", include("apps.employees.api.urls")),
    path("projects/", include("apps.projects.api.urls")),
    path("tasks/", include("apps.tasks.api.urls")),
    path("notifications/", include("apps.notifications.api.urls")),
    path("telegram/", include("apps.telegram.api.urls")),
    path("comments/", include("apps.comments.api.urls")),
    path("files/", include("apps.files.api.urls")),
    path("dashboard/", include("apps.dashboard.api.urls")),
    path("clients/", include("apps.clients.api.urls")),
    path("website/", include("apps.website.api.urls")),
    path("crm/", include("apps.crm.api.urls")),
    path("ai/", include("apps.ai.api.urls")),
]

"""Accounts API routes."""

from django.urls import path

from apps.accounts.api.views import (
    MePasswordView,
    MeView,
    UserDetailView,
    UserListCreateView,
)

app_name = "accounts"

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("me/password/", MePasswordView.as_view(), name="me-password"),
    path("users/", UserListCreateView.as_view(), name="user-list"),
    path("users/<uuid:uuid>/", UserDetailView.as_view(), name="user-detail"),
]

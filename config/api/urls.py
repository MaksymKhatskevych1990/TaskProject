"""Top-level API URL configuration."""

from django.urls import include, path

from apps.website.api.views import ContactLeadView

app_name = "api"

urlpatterns = [
    path("v1/", include("config.api.v1.urls")),
    path("contact/", ContactLeadView.as_view(), name="contact"),
]

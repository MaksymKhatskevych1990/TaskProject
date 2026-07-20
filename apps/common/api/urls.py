"""Infrastructure health routes."""

from django.urls import path

from apps.common.api.views import LivenessView, ReadinessView

app_name = "health"

urlpatterns = [
    path("", LivenessView.as_view(), name="liveness"),
    path("ready/", ReadinessView.as_view(), name="readiness"),
]

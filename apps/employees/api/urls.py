"""Employees API routes."""

from django.urls import path

from apps.employees.api.views import (
    EmployeeDetailView,
    EmployeeListCreateView,
    PositionDetailView,
    PositionListCreateView,
    TeamDetailView,
    TeamListCreateView,
)

app_name = "employees"

urlpatterns = [
    path("positions/", PositionListCreateView.as_view(), name="position-list"),
    path(
        "positions/<uuid:uuid>/",
        PositionDetailView.as_view(),
        name="position-detail",
    ),
    path("teams/", TeamListCreateView.as_view(), name="team-list"),
    path("teams/<uuid:uuid>/", TeamDetailView.as_view(), name="team-detail"),
    path("", EmployeeListCreateView.as_view(), name="employee-list"),
    path("<uuid:uuid>/", EmployeeDetailView.as_view(), name="employee-detail"),
]

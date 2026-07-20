"""Tasks API routes."""

from django.urls import path

from apps.tasks.api.views import TaskDetailView, TaskListCreateView

app_name = "tasks"

urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list"),
    path("<uuid:uuid>/", TaskDetailView.as_view(), name="task-detail"),
]

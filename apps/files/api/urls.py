"""Files API routes."""

from django.urls import path

from apps.files.api.views import TaskAttachmentDetailView, TaskAttachmentListCreateView

app_name = "files"

urlpatterns = [
    path(
        "tasks/<uuid:uuid>/attachments/",
        TaskAttachmentListCreateView.as_view(),
        name="task-attachment-list",
    ),
    path(
        "tasks/<uuid:uuid>/attachments/<uuid:attachment_uuid>/",
        TaskAttachmentDetailView.as_view(),
        name="task-attachment-detail",
    ),
]
